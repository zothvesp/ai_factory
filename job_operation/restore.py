import os
from sqlbak.job_operation.trace import RestoreTracer
from sqlbak.logger import log_module_method
from sqlbak.process_managment.helper import set_subservice_title
import sqlbak.config.agent_settings
from sqlbak.dbms.dbms import DBMS
from sqlbak.destinations.destination import Destination
from sqlbak.definitions import OPERATION_SHORT_CODE_RESTORE, PROCESS_TYPES, SQL_SCRIPT_TYPE
from sqlbak.helpers.temporary_directory import create_sub_directory, create_temp_dir, remove_temp_resource
from sqlbak.local_db import local_db_instanse
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.app_output import APP_OUTPUT
from sqlbak.helpers.files import is_archive, decompress
from sqlbak.helper import helper_instanse

@log_module_method
def handle_restore_message(message):
    job_credential_id = message["JobCredentialsId"] if "JobCredentialsId" in message else None
    object_id = message["BackupObjectId"]
    scripts = message["Scripts"] if "Scripts" in message else {}
    message_id = message["MessageId"]
    object_name = message["ObjectName"]
    local_sql_server_settings = message["LocalSqlServerSettings"] if "LocalSqlServerSettings" in message else None
    restore_folder = None
    archive_password = message["ArchivesPassword"]
    try:
        try:
            trace = RestoreTracer(message_id, object_id, object_name, job_credential_id)
            set_subservice_title("restore-{0}".format(trace.restore_id))
            local_db_instanse.add_process(os.getpid(), trace.restore_id, object_id, PROCESS_TYPES["RESTORE_BACKUP"])
            restore_folder = create_temp_dir(message_id, OPERATION_SHORT_CODE_RESTORE)
            backups = get_backup_for_restore(object_id, message["DestinationInfo"]["DestinationId"])
            destination_info = message["DestinationInfo"]
            PrepareBackupObjects(backups, destination_info["DestinationId"])
            backups = sorted(backups, key=(lambda backup: backup["BackupOject"]["ObjectType"]))
            trace.download_start()
            DownloadBackups(backups, destination_info, create_sub_directory(restore_folder, object_name))
            trace.download_finish()
            trace.uncompress_start()
            UncompressBackups(backups, create_sub_directory(restore_folder, object_name + "_u"), archive_password)
            trace.uncompress_finish()
            trace.restore_start()
            RestoreBackups(backups, job_credential_id, object_id, scripts, object_name, local_sql_server_settings, trace.restore_id)
            trace.restore_end()
        except Exception as e:
            try:
                trace.failed(str(e))
                raise e
            finally:
                e = None
                del e

    finally:
        local_db_instanse.delete_process_by_pid(os.getpid())
        if restore_folder is not None:
            remove_temp_resource(restore_folder)


@log_module_method
def cleanup_files(backupObjectFiles):
    for x in backupObjectFiles:
        remove_temp_resource(x)


@log_module_method
def get_backup_for_restore(object_id, destination_id):
    response = remoute_server_request_instanse.get_backups_for_restore(sqlbak.config.agent_settings.get_agent_key(), object_id, destination_id)
    if not response["IsSuccess"]:
        raise Exception(APP_OUTPUT["FAILED_GET_BACKUP_OBJECT"].format(response["ErrorMessage"]))
    return response["Data"]


def execute_scripts(dbms_params, scripts, script_behavior_type='ScriptsAfter'):
    result = ""
    scripts_after = scripts.get(script_behavior_type, [])
    dbms = DBMS(dbms_params)
    db_instance = dbms.get_db_server_class_instance()
    for script in scripts_after:
        if script["ScriptType"] == SQL_SCRIPT_TYPE:
            result += db_instance.handle_scripts(script["Text"], script["Timeout"])
        print(result)
        return result


@log_module_method
def RestoreBackups(backups, job_credential_id, object_id, scripts, object_name, local_sql_server_settings, restore_id):
    agent = local_db_instanse.get_current_agent()
    connection = local_db_instanse.get_connection_by_job_cred_id(job_credential_id)
    path_to_full_backup = None
    dbms_params = {'ServerType':connection["ServerType"], 
     'ConnectionType':connection["ConnectionType"], 
     'Password':connection["Password"], 
     'Host':connection["Host"], 
     'SshHost':connection["SshHost"], 
     'SshPort':connection["SshPort"], 
     'SshUser':connection["SshUser"], 
     'SshLocalMappedPort':connection["SshLocalMappedPort"], 
     'SshPassword':connection["SshPassword"], 
     'Port':connection["Port"], 
     'User':connection["User"], 
     'UseSsh':connection["UseSsh"], 
     'UtilsPath':agent["UtilsPath"], 
     'ObjectName':object_name}
    execute_scripts(dbms_params, scripts, "ScriptsBefore")
    for idx, backup in enumerate(backups):
        dbms_params["BackupType"] = helper_instanse.get_backup_type_by_object_type(backup["BackupOject"]["ObjectType"])
        dbms = DBMS(dbms_params)
        path_to_backup = backup["BackupFiles"][0] if len(backup["BackupFiles"]) == 1 else backup["BackupFiles"]
        if path_to_full_backup == None:
            path_to_full_backup = path_to_backup
        last_backup = len(backups) == idx + 1
        dbms.restore_backup({'backup':{'NewDatabaseName':object_name, 
          'OldDatabaseName':backup["BackupOject"]["ObjectName"], 
          'LocalSqlServerSettings':local_sql_server_settings}, 
         'agent':agent, 
         'restore_id':restore_id, 
         'path_to_backup':path_to_backup, 
         'object_id':object_id, 
         'is_last_backup':last_backup, 
         'scripts':scripts, 
         'path_to_full_backup':path_to_full_backup, 
         'is_first_backup':idx == 0, 
         'is_second_backup':idx == 1})
    else:
        execute_scripts(dbms_params, scripts, "ScriptsAfter")


@log_module_method
def UncompressBackups(backups, uncompress_folder, archive_password):
    for backup in backups:
        backupObjectFiles = backup["BackupFiles"]
        if len([x for x in backupObjectFiles if not x.endswith("zip00") if x.endswith("7z00")]) > 0 or is_archive(backupObjectFiles):
            password = backup["BackupOject"]["password"] if "password" in backup["BackupOject"] else archive_password.strip()
            backup["BackupFiles"] = decompress(backupObjectFiles, uncompress_folder, password)
            cleanup_files(backupObjectFiles)


@log_module_method
def DownloadBackups(backups, destination_info, backup_object_dir):
    for backup in backups:
        archive_files = []
        for file in backup["BackupOject"]["ObjectFileInfos"]:
            archive_files += [download_file(destination_info, backup["BackupOject"]["Folder"], file["FileName"], backup_object_dir, file["OutId"])]
        else:
            backup["BackupFiles"] = archive_files


@log_module_method
def download_file(storage_info, storage_folder, file_name, temporary_folder, outId):
    downloaded_file_path = temporary_folder + "/" + file_name
    destination = Destination()
    storage_info.update({"DestinationPath": storage_folder})
    destination_instance = destination.get_destination_instance(storage_info)
    destination_instance.connect()
    destination_instance.download_file(file_name, temporary_folder + "/", outId)
    return downloaded_file_path


@log_module_method
def PrepareBackupObjects(backups, destionatin_id):
    for backup in backups:
        backup_objects = [x for x in backup["BackupObjects"] if x["DestinationId"] == destionatin_id]
        if len(backup_objects) == 0:
            raise Exception("Destination in message and Destination in backups object not equeles")
        else:
            backup["BackupOject"] = backup_objects[0]
        backupObject = backup_objects[0]
        backup["BackupOject"] = backupObject

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/job_operation/restore.pyc
