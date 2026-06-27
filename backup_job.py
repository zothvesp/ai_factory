
import time, os
from datetime import datetime
from psutil import version_info
from sqlbak.helpers.files import split_file
from sqlbak.exchange_message.helper import IsIntensiveMode
import xml.etree.ElementTree as Et
from sqlbak.definitions import COMPRESSION_LEVELS, BACKUP_TYPES, MONGO_CONST, E7Zip_EXT, ZIP_EXT, CONFIG, DESTINATIONS_CONSTS, MYSQL_CONST, PREVIOUS_BACKUP_HAS_FAILED, MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL, MARIADB_CONST, MSSQL_CONST
from sqlbak.definitions import MESSAGE_TYPES_CONSTS, DESTINATIONS_NAMES, COMPRESSION_PRIORITY_DEFAULT, LOG_BACKUP_CONST, INC_BACKUP_CONST, MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR, MSSQL_DOUBLE_LOG_SAME_MINUTE, FULL_AND_FIRST_BACKUP
from sqlbak.definitions import RESTORE_STATUSES, FOLDER_BACKUP_CONST, SEVERITY_PARAMS, FULL_BACKUP_CONST, TIMEOUT, HOUR_IN_MINUTES, MINUTE_IN_SEC, MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG, MYSQL_DATA_SCHEMA_HAS_CHANGED, PREVIOUS_BACKUP_DOES_NOT_EXISTS, BACKUP_TYPE_CHANGED
from sqlbak.job import Job
from sqlbak.dbms.dbms import DBMS
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_method, log_only_exception
from sqlbak.violation import Violation
from sqlbak.job_trigger import JobTrigger
from sqlbak.cleanup import Cleanup
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import FolderBackupError, CompressError
from sqlbak.helpers.temporary_directory import create_directory, get_correct_path, remove_temp_resource
from sqlbak.helpers.folder_backup import backup_folder

class BackupJob(Job):

    def __init__(self):
        self.native_command = NativeCommand()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        Job.__init__(self)

    @log_method
    def run_backup_job(self, job_params):
        try:
            try:
                self.callback(job_params)
                self.get_initial_settings(job_params)
                self.begin_job()
                self.set_job_settings()
                self.violation = Violation(self.params["UserFullName"])
                self.violation.check_job_plan_violation(job_params["JobId"])
                create_directory(self.params["PathToBackup"])
                if self.params["IsJobScriptEnabled"]:
                    self.run_scripts_before_backup()
                self.create_sql_backup_compress_and_send_to_destinations()
                self.reset_object_backup_result()
                self.create_folder_backup_compress_and_send_to_destination()
                self.send_backups_to_destinations_after_all_backups()
                self.local_db.update_backup(self.params["BackupId"], self.params["CountJobErrors"] == 0)
                self.handle_active_mode()
                self.delete_overdue_backups()
                if self.params["IsJobScriptEnabled"]:
                    self.run_scripts_after_backup()
                if self.params["IsSilentMode"]:
                    if self.params["CountJobErrors"] == 0:
                        self.cleanup_backup_job_logs()
                if len(self.params["JobTriggers"]) > 0:
                    self.send_unsend_backup_logs(self.params["BackupId"], self.params["JobMode"])
                    self.run_job_triggers()
            except Exception as e:
                try:
                    self.catch_job_error(str(e))
                finally:
                    e = None
                    del e

        finally:
            if "PathToBackup" in self.params:
                try:
                    remove_temp_resource(self.params["PathToBackup"])
                except Exception as e:
                    try:
                        self.catch_job_error(e)
                    finally:
                        e = None
                        del e

            self.send_unsend_backup_logs(self.params["BackupId"], self.params["JobMode"])
            self.set_object_backup_result()
            self.end_job()

        return self.params["CountJobErrors"] == 0

    @log_method
    def send_backups_to_destinations_after_all_backups(self):
        if not self.params["BackupOneAndSend"]:
            for backup in self.params["ObjectBackupResults"]:
                if backup["is_success"]:
                    destinations = self.send_backup_to_destinations(backup)
                    backup["destinations"] = destinations

    @log_method
    def send_backup_to_destination_after_backup(self, backup_files, object_type, name, is_not_double_backup):
        backup = {'object_type':object_type, 
         'backup_files':backup_files, 
         'object_name':name, 
         'size':self.params["Size"] if ("Size" in self.params) else 0, 
         'archive_size':self.params["ArchiveSize"] if ("ArchiveSize" in self.params) else 0, 
         'is_not_double_backup':is_not_double_backup}
        return self.send_backup_to_destinations(backup)

    @log_method
    def create_sql_backup_compress_and_send_to_destinationsParse error at or near `LOAD_FAST' instruction at offset 0

    @log_method
    def run_scripts_before_backup(self):
        try:
            dbms = DBMS(self.params)
            dbms.run_scripts_before_backup()
        except Exception as e:
            try:
                self.catch_job_error(self.cm["FAILED_RUN_SCRIPT_BEFORE_BACKUP"].format(str(e)))
            finally:
                e = None
                del e

    def check_if_database_exists(self, database_name):
        dbms = DBMS(self.params)
        return database_name in dbms.get_databases_names()

    @log_method
    def run_scripts_after_backup(self):
        try:
            dbms = DBMS(self.params)
            dbms.run_scripts_after_backup()
        except Exception as e:
            try:
                self.catch_job_error(self.cm["FAILED_RUN_SCRIPT_AFTER_BACKUP"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def create_backup_and_return_backup_name(self, database_data):
        """
        A method to make a database backup
        :param dbms: object
        :param db_name: string
        :param backup_name: string
        :return: None
        """
        if database_data["ShouldGetDumpChecksum"]:
            self.save_checksum_for_dump(database_data["DatabaseName"])
        self.run_dbms_backup(database_data)
        database_data = self.handle_sql_schema(database_data)
        return database_data["BackupName"]

    @log_method
    def run_dbms_backup(self, database_data):
        dbms = DBMS(self.params)
        dbms.backup(database_data, self.params["PathToBackup"])

    @log_method
    def save_checksum_for_dump(self, db_name):
        dbms = DBMS(self.params)
        dump_checksum = dbms.calculate_and_return_checksum_for_file(db_name, self.params["JobId"])
        self.local_db.save_checksum_for_dump_filedump_checksumdb_nameself.params["JobId"]

    @log_method
    def handle_sql_schema(self, database_data):
        if self.params["ServerType"] in (MYSQL_CONST, MARIADB_CONST):
            if database_data["CurrentBackupType"] == INC_BACKUP_CONST:
                dbms = DBMS(self.params)
                res = dbms.check_if_mysql_schema_has_changed(database_data, self.params["JobId"], self.params["PathToBackup"], self.params["FileNameFormat"], self.params["BackupAt"])
                database_data["BackupName"] = res["backup_name"]
                self.params["BackupType"] = res["backup_type"]
                if res["is_schema_changed"]:
                    self.run_dbms_backup(database_data)
        return database_data

    @log_method
    def get_backup_size(self, db, is_not_double_backup):
        if is_not_double_backup:
            self.params["Size"] = self.helper.get_resource_size(self.params["PathToBackup"] + db["BackupName"] + db["BackupExtension"])
            self.params["GeneralSize"] += int(self.params["Size"])
            self.local_db.update_backup_size(self.params["BackupId"], self.params["Size"])
        self.params = self.job_log.backup_complete_logself.paramsdb["DatabaseName"](db["BackupName"] + db["BackupExtension"])

    @log_method
    def compress_backup(self, backup_name, idx, backup_extension, is_mysql_inc):
        if not self.params["IsCompressionEnabled"]:
            if self.params["ServerType"] == MONGO_CONST or is_mysql_inc:
                self.params = self.job_log.compress_backup_log(self.params, self.params["PathToBackup"] + backup_name + backup_extension)
                self.compress_file(self.params["PathToBackup"], backup_name, self.params["CompressedBackupExtension"], backup_extension, idx)
                backup_files = self.get_backup_filesself.params["PathToBackup"]backup_nameidx
                self.params = self.job_log.compress_backup_complete_log(self.params, ",".join([x["name"] for x in backup_files]))
        else:
            self.params["ArchiveSize"] = self.helper.get_resource_size(self.params["PathToBackup"] + backup_name + backup_extension)
            self.params["GeneralArchiveSize"] += int(self.params["ArchiveSize"])
            backup_files = [
             {'name':backup_name + backup_extension, 
              'size':self.params["ArchiveSize"],  'path_to_file':self.params["PathToBackup"]}]
        return backup_files

    @log_method
    def get_backup_files_list(self, list_of_files):
        backup_files = []
        for path_of_file in list_of_files:
            path_to_directory_with_file, file_name = os.path.split(path_of_file)
            file_size = self.helper.get_resource_size(path_of_file)
            backup_files.append({'name':file_name, 
             'size':file_size, 
             'path_to_file':path_to_directory_with_file + "/"})
        else:
            return backup_files

    @log_method
    def get_backup_files(self, path_to_backup, backup_name, idx):
        backup_files = []
        for f in self.helper.get_files_in_directory(path_to_backup + str(idx)):
            if backup_name in f:
                path_to_file = path_to_backup + str(idx) + "/"
                file_size = self.helper.get_resource_size(path_to_file)
                backup_files.append({'name':f, 
                 'size':file_size, 
                 'path_to_file':path_to_file})
            return backup_files

    @log_method
    def compress_file(self, path_to_backup, backup_name, compress_extension, backup_extension, idx):
        """
        Method to compress backup
        :return: None
        """
        try:
            create_directory(path_to_backup + str(idx))
            if compress_extension is None:
                compress_extension = ZIP_EXT
            path_to_compressed_backup = path_to_backup + str(idx) + "/" + backup_name + compress_extension
            path_to_original = path_to_backup + backup_name + backup_extension
            compression_level = COMPRESSION_LEVELS[self.params["CompressionEngine"]][self.params["CompressionLevel"]]
            zip_command = self.native_command.compress_backup(self.params["CompressionEngine"], compression_level, self.params["CompressionPassword"], self.params["IsEncryptionEnabled"], path_to_compressed_backup, path_to_original, backup_name, path_to_backup, self.params["CompressionCommandLineOptions"])
            self.params["ArchiveSize"] = self.helper.get_resource_size(path_to_compressed_backup)
            self.params["GeneralArchiveSize"] += int(self.params["ArchiveSize"])
            self.split_compressed_backup(path_to_compressed_backup)
            self.set_process_priority(zip_command)
            self.helper.remove_file_or_dir([path_to_original])
            self.local_db.update_backup_archive_size(self.params["BackupId"], self.params["ArchiveSize"])
        except Exception as e:
            try:
                raise CompressError(e)
            finally:
                e = None
                del e

    @log_method
    def split_compressed_backup(self, path_to_backup):
        if self.params["ArchiveSize"] > self.params["CompressionMaxFileSize"]:
            self.native_command.split_resourceself.params["CompressionMaxFileSize"]path_to_backuppath_to_backup
            self.helper.remove_file_or_dir([path_to_backup])

    @log_method
    def set_process_priority(self, command):
        if self.params["CompressionPriority"] != COMPRESSION_PRIORITY_DEFAULT:
            for pid in self.helper.get_processes_id_by_name(command):
                self.helper.set_process_priority(self.params["CompressionPriority"], pid)

    @log_method
    def send_backup_to_destinations(self, backup):
        """
        Method to send compressed database backup to a destination
        :return: None
        """
        destinations = []
        if len(self.params["Destinations"]) == 0:
            raise Exception(self.cm["INVALID_DESTINATIONS"])
        does_backup_sent_at_least_once = False
        for destination in self.params["Destinations"]:
            try:
                try:
                    sended = False
                    destination["is_success"] = False
                    is_allowed_type = int(backup["object_type"]) in destination["settings"]["SendBackupTypes"]
                    should_sent = not does_backup_sent_at_least_once or destination["is_extreme"] == 0
                    if is_allowed_type:
                        if should_sent:
                            for backup_file in backup["backup_files"]:
                                destination_settings = self.job_settings.get_destination_settings_by_job_id(self.params["JobId"], destination["destination_id"])
                                if backup["is_not_double_backup"]:
                                    outid = self.send_backup_to_destinationbackup_file["name"]destination_settingsbackup_file["path_to_file"]
                                    backup_file["outid"] = outid
                                sended = True
                            else:
                                does_backup_sent_at_least_once = True

                    destination["is_success"] = True
                except Exception as e:
                    try:
                        msg = self.cm["FAILED_SEND_BACKUP"].format(DESTINATIONS_NAMES[destination["settings"]["DestinationType"]], str(e))
                        self.catch_job_error(msg)
                    finally:
                        e = None
                        del e

            finally:
                if sended:
                    self.save_backup_object_and_files(backup, destination)
                destinations.append(destination)

        else:
            return destinations

    @log_method
    def save_backup_object_and_files(self, backup, destination):
        backup_object = self.local_db.add_backup_objectself.paramsbackupdestinationdestination["is_success"]
        for backup_file in backup["backup_files"]:
            self.local_db.add_backup_object_file(backup_object["BackupObjectId"], backup_file["name"], True, backup_file["size"], backup_file["outid"])

    @log_method
    def send_backup_to_destination(self, backup_name, destination, path_to_file):
        """

        :param backup_name: str
        :param destination: dict
        :return:
        """
        self.params = self.job_log.open_destination_connection_log(self.params, destination["settings"])
        self.helper.run_method_with_number_attempts_and_timeout((destination["instance"]), "connect", is_instance=True, attempts=4, time_out=(2 * TIMEOUT))
        self.params = self.job_log.send_files_to_destination_logbackup_nameself.paramsdestination["settings"]
        start_time = datetime.now()
        outid = self.helper.run_method_with_number_attempts_and_timeout((destination["instance"]), "send_backup_to_destination", params=(path_to_file, backup_name), is_instance=True, attempts=4, time_out=(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC))
        self.get_upload_speed(start_time)
        if "VerifyFile" in destination["settings"]:
            if destination["settings"]["VerifyFile"]:
                destination["instance"] = self.get_destination_instance(destination)
                self.verify_files_after_uploading_to_destinationdestination["instance"]backup_nameoutid
        self.params = self.job_log.close_connection_destination_logself.paramsdestination["settings"]["DestinationPath"]destination["settings"]["DestinationType"]
        self.helper.run_method_with_number_attempts_and_timeout((destination["instance"]), "close_connection", is_instance=True, attempts=4, time_out=TIMEOUT)
        return outid

    @log_method
    def get_destination_instance(self, destination):
        if destination["settings"]["DestinationType"] in (DESTINATIONS_CONSTS["GOOGLE"], DESTINATIONS_CONSTS["ONEDRIVE"], DESTINATIONS_CONSTS["ONEDRIVE_BUSINESS"]):
            d = self.job_settings.get_destination_settings_by_job_id(self.params["JobId"], destination["destination_id"])
            destination["instance"] = d["instance"]
        return destination["instance"]

    @log_method
    def get_upload_speed(self, start_time):
        end_time = datetime.now()
        upload_duration = (end_time - start_time).total_seconds()
        bytes_per_sec = self.params["ArchiveSize"] / (1 if upload_duration == 0 else upload_duration)
        uploaded_speed = self.helper.approximate_size(bytes_per_sec)
        self.params = self.job_log.progress_send_files_to_destination_logself.params100(str(uploaded_speed) + "/s")

    @log_method
    def verify_files_after_uploading_to_destination(self, destination_instance, backup_name, outId):
        try:
            self.params = self.job_log.verify_file(self.params, backup_name)
            time.sleep(5)
            is_file_exist = self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "is_file_exist", params=(backup_name, outId), is_instance=True, attempts=4, time_out=(2 * TIMEOUT))
            if not is_file_exist:
                msg = self.cm["FILE_NOT_EXISTS_DEST"].format(str(backup_name))
                self.params = self.job_log.verifying_file_failed(self.params, msg)
                raise Exception(msg)
        except Exception as e:
            try:
                self.catch_job_warning(str(e))
            finally:
                e = None
                del e

    @log_method
    def create_folder_backup_compress_and_send_to_destination(self):
        if not self.params["IsFolderBackupEnabled"]:
            return
        if "BackupType" in self.params:
            if "FolderBackupTypes" in self.params:
                str_backup_type = str(BACKUP_TYPES[self.params["BackupType"]])
                folder_backup_types = self.params["FolderBackupTypes"]
                if str_backup_type not in folder_backup_types:
                    return
        for idx, folder in enumerate(self.params["FolderBackups"]):
            list_of_compressed_backup_files = []
            destinations = []
            is_success = False
            try:
                try:
                    self.params["BackupType"] = FOLDER_BACKUP_CONST
                    folder_path = get_correct_path(folder["path"])
                    self.params = self.job_log.folder_backup_log(self.params, folder_path)
                    self.params = self.job_log.compress_folder_backup_log(self.params)
                    temp_folder = self.params["PathToBackup"]
                    compression_level = COMPRESSION_LEVELS[self.params["CompressionEngine"]][self.params["CompressionLevel"]]
                    path_to_backup, backup_file_name = backup_folder(folder_path, temp_folder, folder["file_name"], self.params["CompressionEngine"], compression_level, self.params["CompressionPassword"], self.params["IsEncryptionEnabled"], self.params["CompressionCommandLineOptions"], idx * 1000)
                    backup_file = os.path.join(path_to_backup, backup_file_name)
                    if self.helper.get_resource_size(backup_file) > self.params["CompressionMaxFileSize"]:
                        list_of_splitted_files = split_file(backup_file, backup_file, self.params["CompressionMaxFileSize"])
                        list_of_compressed_backup_files = self.get_backup_files_list(list_of_splitted_files)
                    else:
                        list_of_compressed_backup_files = self.get_backup_files_list([backup_file])
                    archive_size = sum([x["size"] for x in list_of_compressed_backup_files])
                    self.params["Size"] = self.helper.get_resource_size(folder_path)
                    self.params["GeneralSize"] += self.params["Size"]
                    self.params["ArchiveSize"] = archive_size
                    self.params["GeneralArchiveSize"] += archive_size
                    self.params = self.job_log.compress_folder_backup_complete_logself.paramsfolder_path[x["name"] for x in list_of_compressed_backup_files]archive_size
                    if self.params["BackupOneAndSend"]:
                        destinations = self.send_backup_to_destination_after_backuplist_of_compressed_backup_filesBACKUP_TYPES["FOLDER"]folder["name"]True
                    is_success = True
                except Exception as e:
                    try:
                        self.catch_job_error(self.cm["FAILED_CREATE_FOLDER_BACKUP"].format(str(FolderBackupError(e))))
                    finally:
                        e = None
                        del e

            finally:
                self.add_backup_object_result_locallyis_successfolder["name"]BACKUP_TYPES["FOLDER"]folder_path
                self.save_object_result_in_paramslist_of_compressed_backup_filesfolder["name"]destinationsis_successFULL_BACKUP_CONSTBACKUP_TYPES["FOLDER"]folder_pathTrue

    @log_method
    def is_folder_adapted_to_backup(self, path_to_folder, folder_name):
        """

        :param path_to_folder:
        :param folder_name:
        :return:
        """
        folder_size = self.helper.get_resource_size(path_to_folder)
        if folder_size > int(self.params["FreeFolderSpace"]):
            return False
        self.params["Size"] = folder_size
        self.params["GeneralSize"] += int(self.params["Size"])
        self.native_command.copy_resource(path_to_folder, self.params["PathToBackup"] + folder_name)
        self.exclude_files_from_folder_backup(folder_name)
        return True

    @log_method
    def exclude_files_from_folder_backupParse error at or near `BUILD_LIST_0' instruction at offset 0

    @log_method
    def handle_active_mode(self):
        if self.job_log.check_and_synk_intensive_mode():
            self.send_backup_object_result_to_remote_server()
            self.send_backup_object_to_remote_server()

    @log_method
    def send_backup_object_result_to_remote_server(self):
        for backup in self.local_db.get_backup_object_results(self.params["BackupId"]):
            data = {'BackupObjectResultId':None,  'BackupId':self.params["BackupRemoteId"], 
             'ObjectType':backup["ObjectType"], 
             'ObjectName':backup["ObjectName"], 
             'FullObjectName':backup["FullObjectName"], 
             'BackupAt':("/Date({0})/".format)(backup["BackupAt"]), 
             'IsSuccess':backup["IsSuccess"], 
             'Status':backup["ObjectStatus"], 
             'BackupObjectResultKey':str(backup["BackupObjectResultKey"])}
            res = self.remote_request.trace_backup_object_result(data, self.params["AgentKey"])
            if not res["IsSuccess"]:
                raise Exception(self.cm["FAILED_TRACE_BACKUP_OBJECT"].format(str(res["ErrorMessage"])))
            else:
                self.local_db.update_backup_object_result_remote_id(res["Data"], backup["BackupObjectResultKey"])

    @log_method
    def send_backup_object_to_remote_server(self):
        """

        :param backup:
        :param destination_setting:
        :return:
        """
        for backupObject in self.local_db.get_backup_objects(self.params["BackupId"]):
            object_settings = self.get_backup_object_settings(backupObject)
            self.trace_and_save_backup_object_file(object_settings, backupObject)

    @log_method
    def get_backup_object_settings(self, backupObject):
        object_files = self.get_object_files(backupObject["Id"])
        backup_at = "/Date({0})/".format(self.helper.get_time_in_milliseconds(backupObject["BackupDate"]))
        is_cleanup_allowed = self.is_cleanup_allowed(backupObject["ObjectType"], self.params["FileNameFormat"])
        settings = {'BackupObjectId':None, 
         'BackupId':self.params["BackupRemoteId"], 
         'DestinationId':int(backupObject["DestinationId"]), 
         'ObjectType':backupObject["ObjectType"], 
         'ObjectName':backupObject["ObjectName"], 
         'IsSuccess':backupObject["IsSuccess"], 
         'Folder':str(backupObject["Folder"]), 
         'BackupAt':backup_at, 
         'ObjectFileInfos':object_files, 
         'BackupObjectKey':str(backupObject["BackupObjectKey"]), 
         'Size':int(backupObject["Size"]), 
         'ArchiveSize':int(backupObject["ArchiveSize"]), 
         'IsCleanupAllowed':is_cleanup_allowed}
        return settings

    @log_method
    def is_cleanup_allowed(self, object_type, file_name_format):
        backup_type = self.helper.get_backup_type_by_object_type(object_type)
        if backup_type in (LOG_BACKUP_CONST, INC_BACKUP_CONST):
            is_cleanup_allowed = file_name_format == "DateAndTime"
        else:
            is_cleanup_allowed = file_name_format in ('DateAndTime', 'Date')
        return is_cleanup_allowed

    @log_method
    def get_object_files(self, backup_id):
        files = self.local_db.get_backup_object_files_by_backup_object_id(backup_id)
        if files is None:
            raise Exception(self.cm["FAILED_SEND_OBJECTS"].format("There are no object files"))
        return [{'BackupObjectFileId':0,  'FileName':f["FileName"],  'OutId':f["OutId"],  'Exist':None,  'FileSize':f["FileSize"]} for f in files]

    @log_method
    def trace_and_save_backup_object_file(self, object_settings, backupObject):
        res = self.remote_request.trace_backup_object(object_settings, self.params["AgentKey"])
        if not res["IsSuccess"]:
            raise Exception(self.cm["FAILED_SEND_OBJECTS"].format(str(res["ErrorMessage"])))
        self.local_db.update_backup_object_remote_id_by_key(res["Data"], backupObject["BackupObjectKey"])

    @log_method
    def run_job_triggers(self):
        job_trigger = JobTrigger(self.params)
        job_trigger.run()

    @log_method
    def delete_overdue_backups(self):
        cleanup = Cleanup(self.params)
        cleanup.clean_old_backups()

    @log_method
    def handle_backup_type(self, database):
        if database["BackupTypeRaiseType"]:
            raise_method = self.get_backup_log_raise_method(database["BackupTypeRaiseType"])
            raise_method(database["BackupTypeRaiseData"])
        self.params.update({'BackupType':database["CurrentBackupType"], 
         'BackupTypeForTrigger':database["CurrentBackupType"]})

    @log_method
    def get_backup_log_raise_method(self, raise_type):
        raise_methods = {PREVIOUS_BACKUP_HAS_FAILED: (self.previous_backup_has_faild_warning), 
         MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR: (self.mssql_backup_chain_is_broken_raise_error), 
         MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG: (self.mssql_backup_chain_is_broken_generate_warning), 
         MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL: (self.mssql_backup_chain_is_broken_make_full), 
         MSSQL_DOUBLE_LOG_SAME_MINUTE: (self.double_log_same_minute), 
         MYSQL_DATA_SCHEMA_HAS_CHANGED: (self.mysql_data_schema_has_changed), 
         BACKUP_TYPE_CHANGED: (self.backup_type_changed), 
         FULL_AND_FIRST_BACKUP: (self.print_empty_log), 
         PREVIOUS_BACKUP_DOES_NOT_EXISTS: (self.previous_backup_does_not_exists_error)}
        return raise_methods[raise_type]

    @log_method
    def previous_backup_has_faild_warning(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.backup_type_changedself.paramsraise_data["DatabaseName"]self.params["JobBackupType"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def mssql_backup_chain_is_broken_raise_error(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Error"]
        self.params = self.job_log.broken_chain_errorself.params"code"raise_data["DatabaseName"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]
        raise Exception(self.cm["BROKEN_CHAIN"])

    @log_method
    def mssql_backup_chain_is_broken_generate_warning(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.broken_chain_warningself.params"code"raise_data["DatabaseName"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def mssql_backup_chain_is_broken_make_full(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.broken_chain_change_backup_typeself.params"code"raise_data["DatabaseName"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def double_log_same_minute(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.backup_type_changedself.paramsraise_data["DatabaseName"]self.params["JobBackupType"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def mysql_data_schema_has_changed(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.data_schema_has_changed(self.params)
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    def backup_type_changed(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.data_schema_has_changed_with_reasonself.paramsraise_data["CurrentBackupType"]raise_data["Reason"]raise_data["DatabaseName"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def previous_backup_does_not_exists_error(self, raise_data):
        self.params["Severity"] = SEVERITY_PARAMS["Error"]
        self.params = self.job_log.backup_type_changedself.paramsraise_data["DatabaseName"]self.params["JobBackupType"]raise_data["CurrentBackupType"]
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def print_empty_log(self, raise_data):
        return

    @log_method
    def add_backup_object_result_locally(self, is_success, name, backup_type, full_name):
        self.local_db.add_backup_object_result({'BackupRemoteId':self.params["BackupRemoteId"], 
         'BackupId':self.params["BackupId"], 
         'ObjectType':backup_type, 
         'ObjectName':name, 
         'BackupAt':(self.helper.get_time_in_milliseconds)(), 
         'IsSuccess':is_success, 
         'Status':1 if is_success else 3, 
         'BackupObjectResultKey':(self.helper.get_uuid)(), 
         'FullObjectName':full_name})

    @log_method
    def save_object_result_in_params(self, backup_files, name, destinations, is_success, backup_type, object_type, full_name, is_not_double_backup):
        self.params["ObjectBackupResults"].append({'backup_type':backup_type, 
         'backup_files':backup_files, 
         'full_object_name':full_name, 
         'archive_size':self.params["ArchiveSize"] if ("ArchiveSize" in self.params) else 0, 
         'size':self.params["Size"] if ("Size" in self.params) else 0, 
         'object_name':name, 
         'object_type':object_type, 
         'destinations':destinations, 
         'is_success':is_success, 
         'status':1 if is_success else 3, 
         'is_not_double_backup':is_not_double_backup})
