from datetime import datetime
from operator import itemgetter
import os, json
from sqlbak.logger import log_method
from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.native_command import NativeCommand
from sqlbak.destinations.destination import Destination
from sqlbak.dbms.dbms import DBMS
from sqlbak.definitions import CONFIG, RESTORE_STATUSES, PROCESS_TYPES, ZIP_EXT, DOWNLOAD_STATUSES, HOUR_IN_MINUTES, MINUTE_IN_SEC, XTRABACKUP_CONST, BACKUP_TYPES, FULL_BACKUP_CONST, INC_BACKUP_CONST
from sqlbak.app_output import APP_OUTPUT
from sqlbak.helpers.permissons import reset_access_for_working_dir
from sqlbak.helpers.temporary_directory import create_directory
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse

class Restore:

    def __init__(self):
        self.local_db = LocalDB()
        self.helper = Helper()
        self.remote_request = RemoteServerRequest()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.native_command = NativeCommand()

    @log_method
    def handle_restore_message(self, message):
        """

        :param message:
        :return:
        """
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            parent_path = self.local_db.get_working_dir()
            working_dir = self.create_temp_directory(parent_path, message["JobCredentialsId"])
            restore_id = self.get_restore_id(message, agent["AgentKey"])
            sorted_backups = sorted((self.get_backups(message, agent, working_dir)), key=(itemgetter("ObjectType")))
            path_to_full_backup = None
            for idx, backup in enumerate(sorted_backups):
                try:
                    for backup_file in backup["BackupObjectFiles"]:
                        self.download_backup_for_restore(backup["DestinationInstance"], backup_file["FileName"], agent["AgentKey"], restore_id, message["BackupObjectId"], backup["TmpWorkingDir"], backup["Folder"], backup_file["OutId"])
                    else:
                        path_to_backup = self.get_uncompress_backup_data(agent["AgentKey"], restore_id, backup, message)
                        if idx == 0:
                            path_to_full_backup = path_to_backup
                        self.check_if_file_exist_locally(path_to_backup)
                        reset_access_for_working_dir()
                        is_last_backup = idx == len(sorted_backups) - 1
                        is_inc_xtrabackup = backup["ObjectType"] == BACKUP_TYPES[FULL_BACKUP_CONST] and backup["Connection"]["ServerType"] == XTRABACKUP_CONST and len(sorted_backups) > 1
                        if is_inc_xtrabackup:
                            backup["ObjectType"] = BACKUP_TYPES[INC_BACKUP_CONST]
                        restore_data = {'backup':backup, 
                         'agent':agent, 
                         'restore_id':restore_id, 
                         'path_to_backup':path_to_backup, 
                         'object_id':message["BackupObjectId"], 
                         'is_last_backup':is_last_backup, 
                         'scripts':message["Scripts"] if ("Scripts" in message) else {}, 
                         'path_to_full_backup':path_to_full_backup, 
                         'is_first_backup':idx == 0, 
                         'is_second_backup':idx == 1}
                        self.restore_backup(restore_data)
                        if is_last_backup:
                            self.clean_temp_data(restore_id, working_dir, backup)

                except Exception as e:
                    try:
                        self.clean_temp_data(restore_id, working_dir, backup)
                        raise Exception(e)
                    finally:
                        e = None
                        del e

        except Exception as e:
            try:
                self.clean_temp_data(restore_id, working_dir)
                if restore_id is not None:
                    self.trace_end_restore_backup(agent["AgentKey"], restore_id, message["BackupObjectId"], RESTORE_STATUSES["FAILED"], str(e))
            finally:
                e = None
                del e

    @log_method
    def create_temp_directory(self, parent_path_to, file_name=None):
        now = datetime.now()
        file_name = "" if file_name is None else "_" + str(file_name)
        working_dir = parent_path_to + file_name + str(now.strftime("%Y%m%d%H%M%S%f")) + "/"
        self.helper.remove_file_or_dir([working_dir])
        create_directory(working_dir)
        return working_dir

    @log_method
    def get_backups(self, message, agent, working_dir):
        """

        :param message:
        :param agent:
        :param working_dir:
        :return:
        """
        backups_from_server = self.get_backups_from_server(agent["AgentKey"], message)
        backups = []
        for backup in backups_from_server:
            for backup_object in backup["BackupObjects"]:
                backup_settings = self.get_backup_settings(working_dir, message, backup_object)
                backups.append(backup_settings)
            else:
                if len(backups) == 0:
                    raise Exception(self.cm["NO_BACKUPS"])
                return backups

    @log_method
    def get_backups_from_server(self, agent_key, message):
        response = self.remote_request.get_backups_for_restore(agent_key, message["BackupObjectId"], message["DestinationInfo"]["DestinationId"])
        if not response["IsSuccess"]:
            raise Exception(self.cm["FAILED_GET_BACKUP_OBJECT"].format(response["ErrorMessage"]))
        return response["Data"]

    @log_method
    def get_backup_settings(self, working_dir, message, backup_object):
        connection = self.local_db.get_connection_by_job_cred_id(message["JobCredentialsId"])
        if connection is None:
            raise Exception(self.cm["FAILED_GET_DBMS_SETTS"])
        tmp_dir = self.create_temp_directory(working_dir, backup_object["ObjectName"])
        destination_instance = self.get_destination_instance(message, backup_object)
        return {'Connection':connection, 
         'DestinationInstance':destination_instance, 
         'NewDatabaseName':message["ObjectName"], 
         'OldDatabaseName':backup_object["ObjectName"], 
         'ArchiveSize':backup_object["ArchiveSize"], 
         'Folder':backup_object["Folder"], 
         'IsSuccess':backup_object["IsSuccess"], 
         'BackupObjectFiles':backup_object["ObjectFileInfos"], 
         'ObjectType':backup_object["ObjectType"], 
         'Size':backup_object["Size"], 
         'TmpWorkingDir':tmp_dir, 
         'DestinationType':message["DestinationInfo"]["DestinationType"], 
         'LocalSqlServerSettings':message["LocalSqlServerSettings"] if ("LocalSqlServerSettings" in message) else None}

    @log_method
    def get_destination_instance(self, message, backup_object):
        destination = Destination()
        message["DestinationInfo"].update({"DestinationPath": (backup_object["Folder"] if backup_object["Folder"] is not None else "")})
        destination_instance = destination.get_destination_instance(message["DestinationInfo"])
        if destination_instance is None:
            raise Exception(self.cm["FAILED_GET_DEST_SETTS"])
        return destination_instance

    @log_method
    def get_restore_id(self, message, agent_key):
        job_credential_id = message["JobCredentialsId"] if "JobCredentialsId" in message else None
        res = remoute_server_request_instanse.trace_begin_restore(agent_key, message["MessageId"], message["BackupObjectId"], message["ObjectName"], RESTORE_STATUSES["CREATED"], None, job_credential_id)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        restore_id = res["Data"]["RestoreId"]
        self.local_db.add_process(os.getpid(), restore_id, message["BackupObjectId"], PROCESS_TYPES["RESTORE_BACKUP"])
        return restore_id

    @log_method
    def download_backup_for_restore(self, destination_instance, file_name, agent_key, restore_id, object_id, working_dir, destination_folder, outId):
        """

        :param destination_instance:
        :param file_name:
        :param agent_key:
        :param restore_id:
        :param backup_object_id:
        :param working_dir:
        :param destination_folder:
        :return:
        """
        self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "connect", is_instance=True, attempts=4, time_out=(5 * MINUTE_IN_SEC))
        self.check_if_backup_exist_at_destination(destination_instance, destination_folder, file_name, outId)
        self.trace_restore(agent_key, restore_id, object_id, RESTORE_STATUSES["DOWNLOADING"], DOWNLOAD_STATUSES["DOWNLOADING"])
        self.download_backup_and_check(working_dir, destination_instance, file_name, outId)
        self.trace_restore(agent_key, restore_id, object_id, RESTORE_STATUSES["DOWNLOADED"], DOWNLOAD_STATUSES["DOWNLOADED"])

    @log_method
    def check_if_backup_exist_at_destination(self, destination_instance, destination_folder, file_name, outId):
        is_file_exist = self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "is_file_exist", params=(file_name, outId), is_instance=True, attempts=4, time_out=(5 * MINUTE_IN_SEC))
        if not is_file_exist:
            raise Exception(self.cm["FILE_NOT_EXISTS_DEST"].format("/" + destination_folder + "/" + file_name))

    @log_method
    def download_backup_and_check(self, working_dir, destination_instance, file_name, outId):
        create_directory(working_dir)
        self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "download_file", params=(file_name, working_dir, outId), is_instance=True, attempts=4, time_out=(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC))
        self.check_if_file_exist_locally(working_dir + file_name)

    @log_method
    def get_uncompress_backup_data(self, agent_key, restore_id, backup, message):
        if self.is_backup_compressed(backup):
            files_in_dir = [f for f in os.listdir(backup["TmpWorkingDir"]) if os.path.isfile(os.path.join(backup["TmpWorkingDir"], f))]
            backup_name = str(backup["NewDatabaseName"]).replace(" ", "_") + ZIP_EXT
            if len(files_in_dir) > 1:
                old_backup_name = str(backup["OldDatabaseName"])
            else:
                old_backup_name = files_in_dir[0]
            self.native_command.join_split_resource(backup["TmpWorkingDir"] + old_backup_name, backup["TmpWorkingDir"] + backup_name)
            uncompress_backup = self.uncompress_backup(message["ArchivesPassword"], backup_name, agent_key, restore_id, message["BackupObjectId"], backup["TmpWorkingDir"])
        else:
            uncompress_backup = backup["TmpWorkingDir"] + backup["BackupObjectFiles"][0]["FileName"]
        return uncompress_backup

    @log_method
    def is_backup_compressed(self, backup):
        if len(backup["BackupObjectFiles"]) == 0:
            raise Exception("Failed to get backup object files")
        file_name = backup["BackupObjectFiles"][0]["FileName"]
        split_file_name = file_name.split(".")
        if len(split_file_name) == 1:
            if backup["ObjectType"] == BACKUP_TYPES[INC_BACKUP_CONST]:
                return False
        return "zip" in split_file_name[-1] or "7z" in split_file_name[-1] or "7z" in split_file_name[-2]

    @log_method
    def uncompress_backup(self, archive_password, file_name, agent_key, restore_id, object_id, working_dir):
        """

        :param archive_password:
        :param file_name:
        :param agent_key:
        :param restore_id:
        :param object_id:
        :param working_dir:
        :return:
        """
        reset_access_for_working_dir()
        self.trace_restore(agent_key, restore_id, object_id, RESTORE_STATUSES["UNCOMPRESSING"], DOWNLOAD_STATUSES["DOWNLOADED"])
        path_to_uncompressed_backup = self.create_temp_directory(working_dir)
        reset_access_for_working_dir()
        password = self.get_password_to_decompress_backup(archive_password)
        if self.native_command.check_installed_util("7z"):
            self.native_command.decompress_by_7zip(working_dir + file_name, path_to_uncompressed_backup, password)
        else:
            splitted_file_name = file_name.split(".")[-1]
            if splitted_file_name == "7z":
                self.native_command.decompress_by_7zip(working_dir + file_name, path_to_uncompressed_backup, password)
            else:
                self.native_command.decompress_by_unzip(working_dir + file_name, path_to_uncompressed_backup, password)
        unzip_backup_file_names = self.helper.get_files_in_directory(path_to_uncompressed_backup)
        if len(unzip_backup_file_names) == 0:
            raise Exception(self.cm["BACKUP_EMPTY"])
        self.trace_restore(agent_key, restore_id, object_id, RESTORE_STATUSES["UNCOMPRESSED"], DOWNLOAD_STATUSES["DOWNLOADED"], str("/Date({}0)/".format(self.helper.get_time_in_milliseconds())))
        return path_to_uncompressed_backup + unzip_backup_file_names[0]

    @log_method
    def get_password_to_decompress_backup(self, archive_password):
        return "{0}".format(str(archive_password) if archive_password.strip() != "" else "")

    @log_method
    def restore_backup(self, restore_data):
        self.trace_restore(restore_data["agent"]["AgentKey"], restore_data["restore_id"], restore_data["object_id"], RESTORE_STATUSES["RESTORING"], DOWNLOAD_STATUSES["DOWNLOADED"])
        dbms_settings = self.get_dbms_settings(restore_data["backup"]["Connection"], restore_data["agent"], restore_data["backup"]["ObjectType"])
        dbms = DBMS(dbms_settings)
        text = dbms.restore_backup(restore_data)
        if restore_data["is_last_backup"]:
            self.trace_end_restore_backup(restore_data["agent"]["AgentKey"], restore_data["restore_id"], restore_data["object_id"], RESTORE_STATUSES["RESTORED"], text)

    @log_method
    def get_dbms_settings(self, connection, agent, object_type):
        return {'ServerType':connection["ServerType"], 
         'ConnectionType':connection["ConnectionType"], 
         'Password':connection["Password"], 
         'Host':connection["Host"], 
         'SshHost':connection["SshHost"], 
         'SshPort':connection["SshPort"], 
         'SshUser':connection["SshUser"], 
         'SshPassword':connection["SshPassword"], 
         'Port':connection["Port"], 
         'User':connection["User"], 
         'UseSsh':connection["UseSsh"], 
         'UtilsPath':agent["UtilsPath"], 
         'BackupType':(self.helper.get_backup_type_by_object_type)(object_type)}

    @log_method
    def trace_end_restore_backup(self, agent_key, restore_id, object_id, status, message):
        res = self.remote_request.trace_end_restore(agent_key, restore_id, object_id, status, DOWNLOAD_STATUSES["DOWNLOADED"], message, "")
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def trace_restore(self, agent_key, restore_id, object_id, restore_status, download_status, date_time=None):
        res = self.remote_request.trace_restore(agent_key, restore_id, object_id, restore_status, download_status, "", "", date_time)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def clean_temp_data(self, restore_id, working_dir, backup=None):
        if working_dir:
            self.helper.remove_file_or_dir([working_dir])
        if backup:
            self.helper.remove_file_or_dir([backup["TmpWorkingDir"]])
        if restore_id is not None:
            self.local_db.delete_process(restore_id, PROCESS_TYPES["RESTORE_BACKUP"])

    @log_method
    def check_if_file_exist_locally(self, path_to_resource):
        if not os.path.exists(path_to_resource):
            raise Exception(self.cm["FILE_NOT_EXISTS"].format(str(path_to_resource)))

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/restore.pyc
