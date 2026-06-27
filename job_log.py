
from os import getpid
import time
from sqlbak.exchange_message.helper import IsIntensiveMode
from sqlbak.trace_event import TraceEvent
import xml.etree.ElementTree as Et
from datetime import datetime
from sqlbak.definitions import DESTINATIONS_NAMES, CONFIG, BACKUP_TYPES, CONSOLE_COLORS, BACKUP_JOB_MODE, LOG_BACKUP_CONST, INC_BACKUP_CONST
from sqlbak.helper import Helper
from sqlbak.logger import log_data, log_error, log_method, log_only_exception
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest

class JobLog:

    def __init__(self):
        self.remote_server = RemoteServerRequest()
        self.local_db = LocalDB()
        self.params = None
        self.helper = Helper()

    def job_log_local(self, params):
        """
        Method to save, log and print backup information
        :param params: dict;
        :return: dict;
        """
        params["BackupLogKey"] = self.helper.get_uuid()
        self.params = self.add_log_info_to_local_db(params)
        if self.params["IsConsoleMode"]:
            self.print_log_job_message(self.params["ActionType"], self.params["LogParams"])
        return self.params

    def check_and_synk_intensive_mode(self):
        """
        Method to check is intensive mode
        :return: bool;
        """
        is_intensive_mode = IsIntensiveMode()
        if is_intensive_mode:
            if self.params["BackupRemoteId"] is None:
                self.params["IsSilentMode"] = False
                remote_id = self.try_sync_log_with_server(self.params["BackupId"], self.params["JobMode"])
                if remote_id:
                    self.params["BackupRemoteId"] = remote_id
        return is_intensive_mode

    @log_only_exception
    def job_log(self, params):
        """
        Method to save, log and print backup information
        :param params: dict;
        :return: dict;
        """
        params["BackupLogKey"] = self.helper.get_uuid()
        self.params = self.add_log_info_to_local_db(params)
        try:
            if self.check_and_synk_intensive_mode():
                self.send_log_info_to_remote_server(self.params)
        except Exception as e:
            try:
                log_error(e, "Error sending log to server.")
                self.helper.print_color_text(str(e), None)
            finally:
                e = None
                del e

        else:
            if self.params["IsConsoleMode"]:
                self.print_log_job_message(self.params["ActionType"], self.params["LogParams"])
            return self.params

    @log_only_exception
    def add_log_info_to_local_db(self, params):
        """

        :param params:
        :return:
        """
        params["BackupLogId"] = self.local_db.add_backup_log(params["BackupId"], params["ActionType"], params["Severity"], params["BackupLogKey"])
        params["BackupLogParamRecords"] = self.local_db.add_backup_log_params(params["BackupLogId"], params["LogParams"])
        return params

    @log_only_exception
    def send_log_info_to_remote_server(self, params):
        """

        :param params:
        :return:
        """
        data = {'BackupId':int(params["BackupRemoteId"]), 
         'BackupLogRecords':[
          {'ActionType':str(params["ActionType"]), 
           'CreatedTime':str("/Date({0})/".format(self.helper.get_time_in_milliseconds())), 
           'Severity':int(params["Severity"]), 
           'BackupLogKey':str(params["BackupLogKey"]), 
           'BackupLogParamRecords':params["BackupLogParamRecords"]}]}
        res = self.remote_server.append_log_records((params["AgentKey"], data))
        if res["IsSuccess"]:
            self.local_db.update_backup_log_remote_id(params["BackupLogId"], params["BackupRemoteId"])
        else:
            raise Exception(str(res["ErrorMessage"]))

    @log_only_exception
    def print_log_job_message(self, action_type, params):
        text = self.helper.get_log_action(CONFIG["LOCALE"], action_type, params)
        self.helper.print_color_text(text, CONSOLE_COLORS["RED"] if "Error" in action_type else None)

    @log_method
    def get_backup_logs_as_xml_string(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        backup_logs = self.local_db.get_backup_logs(backup_id)
        if len(backup_logs) > 0:
            offset = self.helper.get_utc_offset()
            log_records_element = Et.Element("BackupLogRecords")
            for backup_log in backup_logs:
                d = self.helper.get_date_time(backup_log["CreatedDate"])
                date_time = "{0:%Y}-{0:%m}-{0:%d}T{0:%H}:{0:%M}:{0:%S}.{0:%f}{1}".format(d, offset)
                log = Et.SubElement(log_records_element, "Record")
                log.attrib["ActionType"] = str(backup_log["ActionType"])
                log.attrib["CreatedTime"] = date_time
                log.attrib["Severity"] = str(backup_log["Severity"])
                log.attrib["BackupLogKey"] = str(backup_log["BackupLogKey"])
                param = Et.SubElement(log, "BackupLogParamRecords")
                for backup_log_param in self.local_db.get_backup_log_params(backup_log["Id"]):
                    param_record = Et.SubElement(param, "Record")
                    param_record.attrib["ParamName"] = str(backup_log_param["ParamName"])
                    param_record.attrib["ParamValue"] = str(backup_log_param["ParamValue"]) if backup_log_param["ParamValue"] is not None else "NULL"
                else:
                    return log_records_element

        return

    @log_method
    def get_backup_objects_as_xml_string(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        offset = self.helper.get_utc_offset()
        object_element = Et.Element("BackupObjectRecords")
        for backup_object in self.local_db.get_backup_objects(backup_id):
            d = self.helper.get_date_time(backup_object["BackupDate"])
            date_time = "{0:%Y}-{0:%m}-{0:%d}T{0:%H}:{0:%M}:{0:%S}.{0:%f}{1}".format(d, offset)
            record = Et.SubElement(object_element, "Record")
            log_data("Destination ID:".format(backup_object["DestinationId"]))
            record.attrib["DestinationId"] = str(backup_object["DestinationId"])
            log_data("ObjectType:".format(backup_object["ObjectType"]))
            record.attrib["ObjectType"] = str(backup_object["ObjectType"])
            log_data("ObjectName:".format(backup_object["ObjectName"]))
            record.attrib["ObjectName"] = str(backup_object["ObjectName"])
            log_data("BackupTime:".format(date_time))
            record.attrib["BackupTime"] = date_time
            log_data("IsSuccess:".format(backup_object["IsSuccess"]))
            record.attrib["IsSuccess"] = "False" if backup_object["IsSuccess"] == 0 else "True"
            log_data("Folder:".format(backup_object["Folder"]))
            record.attrib["Folder"] = str(backup_object["Folder"])
            log_data("Size:".format(backup_object["Size"]))
            record.attrib["Size"] = str(backup_object["Size"])
            log_data("ArchiveSize:".format(backup_object["ArchiveSize"]))
            record.attrib["ArchiveSize"] = str(backup_object["ArchiveSize"])
            log_data("BackupObjectKey:".format(backup_object["BackupObjectKey"]))
            record.attrib["BackupObjectKey"] = str(backup_object["BackupObjectKey"])
            object_file_records = Et.SubElement(record, "BackupObjectFileRecords")
            for backup_object_file in self.local_db.get_backup_object_files(backup_object["Id"]):
                log_data("Object File Name:".format(backup_object_file["FileName"]))
                log_data("Object File Exist:".format(backup_object_file["Exist"]))
                log_data("Object File Size:".format(backup_object_file["FileSize"]))
                object_file_record = Et.SubElement(object_file_records, "Record")
                object_file_record.attrib["FileName"] = str(backup_object_file["FileName"])
                object_file_record.attrib["Exist"] = "False" if backup_object_file["Exist"] == 0 else "True"
                object_file_record.attrib["FileSize"] = str(backup_object_file["FileSize"])
                if backup_object_file["OutId"] is not None:
                    object_file_record.attrib["OutId"] = str(backup_object_file["OutId"])
            else:
                return object_element

    @log_method
    def get_backup_object_result_as_xml_string(self, backup_id):
        """

        :param backup_id:
        :return:
        """
        offset = self.helper.get_utc_offset()
        result_element = Et.Element("BackupObjectResultRecords")
        for backup in self.local_db.get_backup_object_results(backup_id):
            d = datetime.fromtimestamp(float(backup["BackupAt"]) / 1000)
            date_time = "{0:%Y}-{0:%m}-{0:%d}T{0:%H}:{0:%M}:{0:%S}.{0:%f}{1}".format(d, offset)
            record = Et.SubElement(result_element, "Record")
            log_data("Object Type:".format(backup["ObjectType"]))
            record.attrib["ObjectType"] = str(backup["ObjectType"])
            log_data("Object Name:".format(backup["ObjectName"]))
            record.attrib["ObjectName"] = str(backup["ObjectName"])
            log_data("Backup Time:".format(date_time))
            record.attrib["BackupTime"] = date_time
            log_data("Is Success:".format(backup["IsSuccess"]))
            record.attrib["IsSuccess"] = "False" if backup["IsSuccess"] == 0 else "True"
            log_data("Object Status:".format(backup["ObjectStatus"]))
            record.attrib["ObjectStatus"] = str(backup["ObjectStatus"])
            log_data("Backup Object Result Key:".format(backup["BackupObjectResultKey"]))
            record.attrib["BackupObjectResultKey"] = backup["BackupObjectResultKey"]
        else:
            return result_element

    @log_method
    def get_backup_as_xml_string(self, backup, backup_object_result_str, backup_object_str, backup_log_str, job_mode):
        """

        :param backup:
        :param backup_object_result_str:
        :param backup_object_str:
        :param backup_log_str:
        :param job_mode:
        :return:
        """
        root = Et.Element("Backup")
        root.attrib["BackupId"] = str(backup["Id"])
        root.attrib["JobId"] = str(backup["JobId"])
        root.attrib["BackupType"] = str(backup["BackupType"])[0].lower()
        root.attrib["IsSuccess"] = "False" if backup["IsSuccess"] == 0 else "True"
        root.attrib["Size"] = str(backup["Size"])
        root.attrib["ArchiveSize"] = str(backup["ArchiveSize"])
        root.attrib["StartTime"] = self.helper.local_time_str_to_UTC_str(backup["StartTime"])
        root.attrib["EndTime"] = self.helper.local_time_str_to_UTC_str(backup["EndTime"]) if backup["EndTime"] is not None else ""
        if backup["MessageId"] is not None:
            root.attrib["MessageId"] = str(backup["MessageId"])
        root.attrib["BackupStatus"] = str(backup["BackupStatus"])
        root.attrib["BackupKey"] = str(backup["BackupKey"])
        root.attrib["Mode"] = str(job_mode)
        job_info = Et.fromstring(backup["JobInfo"].encode("utf-16"))
        root.attrib["IsCleanupAllowed"] = str(self.is_cleanup_allowed(backup["BackupType"], job_info))
        root.attrib["IsEncrypted"] = str(False)
        for job in job_info:
            if job.tag == "CompressionInfo":
                root.attrib["IsEncrypted"] = str(self.helper.is_text_true(job.attrib["IsEncryptionEnabled"]) if "IsEncryptionEnabled" in job.attrib else False)
            root.attrib["JobCredentialsId"] = str(backup["JobCredentialsId"] if backup["JobCredentialsId"] is not None else "NULL")
            root.append(backup_object_result_str)
            root.append(backup_object_str)
            root.append(backup_log_str)
            return root

    @log_method
    def is_cleanup_allowed(self, backup_type, job_info):
        is_cleanup_allowed = True
        if "OutputFileNameFormat" in job_info.attrib:
            if backup_type in (LOG_BACKUP_CONST, INC_BACKUP_CONST):
                is_cleanup_allowed = job_info.attrib["OutputFileNameFormat"] == "DateAndTime"
            else:
                is_cleanup_allowed = job_info.attrib["OutputFileNameFormat"] in ('DateAndTime',
                                                                                 'Date')
        return is_cleanup_allowed

    @log_method
    def update_backup_remote_id(self, data):
        """
        Method to renew remote id of all backup log records
        :param data: xml string; Log records
        :return: None
        """
        try:
            xml = Et.fromstring(data.encode("utf-16"))
            remoute_backup_id = xml.attrib["BackupId"]
            backup_key = xml.attrib["BackupKey"]
            self.local_db.update_backup_remote_id_by_key(remoute_backup_id, backup_key)
            self.local_db.mark_backup_as_sent(backup_key)
            for root in xml:
                if root.tag == "BackupObjectResultResponses":
                    for child in root:
                        self.local_db.update_backup_object_result_remote_id(child.attrib["BackupObjectResultId"], child.attrib["BackupObjectResultKey"])

                elif root.tag == "BackupObjectResponses":
                    for child in root:
                        self.local_db.update_backup_object_remote_id_by_key(child.attrib["BackupObjectId"], child.attrib["BackupObjectKey"])

                elif root.tag == "BackupLogResponses":
                    for child in root:
                        self.local_db.update_backup_log_remote_id_by_key(child.attrib["BackupLogId"], child.attrib["BackupLogKey"])
                    else:
                        return                         return remoute_backup_id

            except Exception as e:
            try:
                TraceEvent().trace_client_error(e, "Can't update backup ID.")
                raise
            finally:
                e = None
                del e

    @log_method
    def get_unsent_backup_log_records(self, backup_id, job_mode):
        """
        Method to get unsent backup log records
        :return: list of log records
        """
        log = self.get_backup_logs_as_xml_string(backup_id)
        if log is None:
            return log
        object_str = self.get_backup_objects_as_xml_string(backup_id)
        object_result = self.get_backup_object_result_as_xml_string(backup_id)
        backup = self.local_db.get_backup_by_id(backup_id)
        if backup is not None:
            result = Et.tostring((self.get_backup_as_xml_string(backup, object_result, object_str, log, job_mode)), encoding="UTF-8").decode("utf-8")
            log_data(result)
            return result

    @log_method
    def push_unsent_logs_to_server(self, logs):
        """

        :param agent_key:
        :param logs:
        :return:
        """
        res = self.remote_server.upload_job_backup_x(logs)
        if not res["IsSuccess"]:
            raise Exception("A try to send a backup log failed. {0}".format(res["ErrorMessage"]))
        return res["Data"]

    @log_only_exception
    def start_backup_log(self, params):
        """

        :param params:
        :return:
        """
        if params["JobMode"] == BACKUP_JOB_MODE["MANUAL"]:
            params["ActionType"] = "Job_Start5"
        else:
            if params["JobMode"] == BACKUP_JOB_MODE["CLI"]:
                params["ActionType"] = "Job_CliStart5"
            else:
                params["ActionType"] = "Job_ScheduledStart5"
        client_version = params["ClientVersion"]
        if not client_version == CONFIG["APP_VERSION"]:
            client_version = client_version + " (" + CONFIG["APP_VERSION"] + ")"
        params["LogParams"] = {'BackupType':params["BackupType"], 
         'JobName':params["JobName"], 
         'ClientName':params["ClientName"], 
         'ClientVersion':client_version, 
         'UserFullName':params["UserFullName"]}
        return self.job_log(params)

    @log_only_exception
    def working_folders_log(self, params):
        params["ActionType"] = "Job_LinuxJobWorkingFolders2"
        params["LogParams"] = {'TempFolder':params["PathToBackup"], 
         'TempDriveFreeSpace':(self.helper.approximate_size)(params["FreeFolderSpace"])}
        return self.job_log(params)

    @log_only_exception
    def backup_complete_log(self, params, db_name, backup_name):
        params["ActionType"] = "Job_BackupDatabaseComplete3"
        params["LogParams"] = {'Database':db_name, 
         'Backup':backup_name, 
         'Size':(self.helper.approximate_size)(params["Size"])}
        return self.job_log(params)

    @log_only_exception
    def compress_backup_log(self, params, file_name):
        params["ActionType"] = "Job_CompressDatabaseBackup3"
        params["LogParams"] = {'Backup':file_name, 
         'ArchiveEngine':params["EncryptionMethod"], 
         'ArchiveEncryption':"Enable" if (params["IsEncryptionEnabled"]) else "Disabled"}
        return self.job_log(params)

    @log_only_exception
    def compress_backup_complete_log(self, params, db_name):
        params["ActionType"] = "Job_CompressDatabaseBackupCompleted2"
        params["LogParams"] = {'Database':db_name, 
         'Volumes':(self.helper.approximate_size)(params["ArchiveSize"])}
        return self.job_log(params)

    @log_method
    def compress_folder_backup_complete_log(self, params, source_path, destination_files, total_size):
        files = ",".join(destination_files)
        params["ActionType"] = "Job_CompressFolderBackupCompleted2"
        params["LogParams"] = {'Path':source_path, 
         'Volumes':(files + " : ") + (self.helper.approximate_size(total_size))}
        return self.job_log(params)

    @log_only_exception
    def open_destination_connection_log(self, params, destination):
        params["ActionType"] = "Dst_OpenConnection2"
        params["LogParams"] = {'Destination':DESTINATIONS_NAMES[destination["DestinationType"]], 
         'Configuration':destination["DestinationPath"] or " "}
        return self.job_log(params)

    @log_only_exception
    def send_files_to_destination_log(self, compressed_backup_name, params, destination):
        params["ActionType"] = "Dst_SendFilesToDestination3"
        params["LogParams"] = {'ObjectName':compressed_backup_name, 
         'Destination':DESTINATIONS_NAMES[destination["DestinationType"]], 
         'Configuration':destination["DestinationPath"] or " "}
        return self.job_log(params)

    @log_only_exception
    def progress_send_files_to_destination_log(self, params, progress_upload, uploaded_file_speed):
        params["ActionType"] = "Dst_SendFilesToDestinationProgress"
        params["LogParams"] = {'ProgressUpload':progress_upload, 
         'Speed':uploaded_file_speed}
        return self.job_log(params)

    @log_only_exception
    def close_connection_destination_log(self, params, destination_path, destination_type):
        params["ActionType"] = "Dst_CloseConnection2"
        params["LogParams"] = {'Destination':DESTINATIONS_NAMES[destination_type], 
         'Configuration':destination_path or " "}
        return self.job_log(params)

    @log_only_exception
    def cleanup_job_log(self, params):
        params["ActionType"] = "Cln_CleanupJob1"
        params["LogParams"] = {"JobName": (params["JobName"])}
        return self.job_log(params)

    @log_only_exception
    def job_finished_with_error_log(self, params):
        params["ActionType"] = "Job_FinishedWithErrors1"
        params["LogParams"] = {"JobName": (params["JobName"])}
        return self.job_log(params)

    @log_only_exception
    def send_error_log_local(self, params, error):
        params["ActionType"] = "Job_RunError1"
        params["LogParams"] = {"Error": (str(error))}
        return self.job_log_local(params)

    @log_only_exception
    def send_error_log(self, params, error):
        params["ActionType"] = "Job_RunError1"
        params["LogParams"] = {"Error": (str(error))}
        return self.job_log(params)

    @log_only_exception
    def folder_backup_log(self, params, folder):
        params["ActionType"] = "Job_BackupFolder2"
        params["LogParams"] = {'Folder':folder, 
         'Path':params["PathToBackup"]}
        return self.job_log(params)

    @log_only_exception
    def compress_folder_backup_log(self, params):
        params["ActionType"] = "Job_CompressFolderBackup2"
        params["LogParams"] = {'ArchiveEngine':params["CompressionEngineFolder"], 
         'Path':params["PathToBackup"]}
        return self.job_log(params)

    @log_only_exception
    def start_maintenance_job_log(self, params):
        params["ActionType"] = "Job_MaintenanceStart4"
        params["LogParams"] = {'JobName':params["JobName"], 
         'ClientName':params["ClientName"], 
         'ClientVersion':params["ClientVersion"], 
         'UserFullName':params["UserFullName"]}
        return self.job_log(params)

    @log_only_exception
    def verifying_file_failed(self, params, error):
        params["ActionType"] = "Sql_VerifyDatabaseWarning1"
        params["LogParams"] = {"Error": (str(error))}
        return self.job_log(params)

    @log_only_exception
    def verify_file(self, params, file_name):
        params["ActionType"] = "Dst_VerifyFile2"
        params["LogParams"] = {'File':file_name, 
         'LocalFile':file_name}
        return self.job_log(params)

    @log_only_exception
    def run_script_before_backup(self, params, msg):
        params["ActionType"] = "Job_RunScriptBeforeBackup1"
        params["LogParams"] = {"Script": (str(msg))}
        return self.job_log(params)

    @log_only_exception
    def run_script_after_backup(self, params, msg):
        params["ActionType"] = "Job_RunScriptAfterBackup1"
        params["LogParams"] = {"Script": msg}
        return self.job_log(params)

    @log_only_exception
    def run_maintenance_job_script(self, params, msg):
        params["ActionType"] = "Job_RunMaintenanceScript1"
        params["LogParams"] = {"Script": msg}
        return self.job_log(params)

    @log_only_exception
    def add_running_job_script_error(self, params, msg, error):
        params["ActionType"] = "SqlBak_ScriptError3"
        params["LogParams"] = {'Script':msg, 
         'Error':error}
        return self.job_log(params)

    @log_only_exception
    def run_job_sql_script_output(self, params, output):
        params["ActionType"] = "Job_SqlScriptOut2"
        params["LogParams"] = {"Text": (str(output)[0[:250]])}
        return self.job_log(params)

    @log_only_exception
    def run_job_bash_script_output(self, params, output):
        params["ActionType"] = "Job_ScriptOutput3"
        params["LogParams"] = {'Script':"cmd", 
         'ExitCode':"Success", 
         'Output':str(output)[0[:250]]}
        return self.job_log(params)

    @log_only_exception
    def clean_old_backup(self, params, object_name, backup_type, backup_time):
        params["ActionType"] = "Cln_DeleteFile3"
        params["LogParams"] = {'ObjectName':str(object_name), 
         'BackupType':str(backup_type), 
         'BackupAt':str(backup_time)}
        return self.job_log(params)

    @log_only_exception
    def cancel_job(self, params, message):
        params["ActionType"] = "Job_JobCancelled1"
        params["LogParams"] = {"Message": (str(message))}
        return self.job_log(params)

    @log_only_exception
    def trace_trigger_restore(self, params, dst_db, src_db, server_name):
        params["ActionType"] = "Job_RestoreDatabaseByTrigger3"
        params["LogParams"] = {'DestinationDatabase':str(dst_db), 
         'Computer':str(server_name), 
         'SourceDatabase':str(src_db)}
        return self.job_log(params)

    @log_only_exception
    def start_restore_by_trigger(self, params):
        params["ActionType"] = "Job_RestoreDatabasesByTrigger"
        params["LogParams"] = {}
        return self.job_log(params)

    @log_only_exception
    def trigger_restore_destination_failed(self, params, dst_db, src_db, server_name, dest_type, dest_config):
        params["ActionType"] = "Job_RestoreDatabaseByTriggerBackupFailed5"
        params["LogParams"] = {'DestinationDatabase':str(dst_db), 
         'Computer':str(server_name), 
         'SourceDatabase':str(src_db), 
         'DestinationType':str(dest_type), 
         'DestinationConfiguration':str(dest_config)}
        return self.job_log(params)

    @log_only_exception
    def failed_to_restore_backup(self, params, src_db, error):
        params["ActionType"] = "Job_FailedRestoreItem"
        params["LogParams"] = {'SourceDatabase':src_db, 
         'Error':error}
        return self.job_log(params)

    @log_only_exception
    def delete_file(self, params, file_name):
        params["ActionType"] = "Dst_DeleteFile1"
        params["LogParams"] = {"File": (str(file_name))}
        return self.job_log(params)

    @log_only_exception
    def backup_type_changed(self, params, database, last_backup_type, current_backup_type):
        params["ActionType"] = "Job_ChangeBackupType4"
        params["LogParams"] = {'LastBackupType':str(last_backup_type), 
         'Database':str(database), 
         'BackupType':str(current_backup_type)}
        return self.job_log(params)

    @log_only_exception
    def broken_chain_error(self, params, code, db_name, backup_type):
        params["ActionType"] = "Job_BrokenChainErrorMessage4"
        params["LogParams"] = {'Code':str(code), 
         'Database':str(db_name), 
         'LastBackupType':str(backup_type), 
         'AppName':CONFIG["APP_NAME"]}
        return self.job_log(params)

    @log_only_exception
    def broken_chain_warning(self, params, code, db_name, backup_type):
        params["ActionType"] = "Job_BrokenChainWarningMessage4"
        params["LogParams"] = {'Code':str(code), 
         'Database':str(db_name), 
         'LastBackupType':str(backup_type), 
         'AppName':CONFIG["APP_NAME"]}
        return self.job_log(params)

    @log_only_exception
    def broken_chain_change_backup_type(self, params, code, db_name, backup_type):
        params["ActionType"] = "Job_BrokenChainChangeBackupTypeMessage4"
        params["LogParams"] = {'Code':str(code), 
         'Database':str(db_name), 
         'LastBackupType':str(backup_type), 
         'AppName':CONFIG["APP_NAME"]}
        return self.job_log(params)

    @log_only_exception
    def file_is_not_found_at_destination(self, params, file_name):
        params["ActionType"] = "Cln_FileNotFound"
        params["LogParams"] = {"Files": file_name}
        return self.job_log(params)

    @log_only_exception
    def folder_is_not_found_at_destination(self, params, folder_name):
        params["ActionType"] = "Cln_FolderNotFound"
        params["LogParams"] = {"Folder": folder_name}
        return self.job_log(params)

    @log_method
    def data_schema_has_changed(self, params):
        params["ActionType"] = "Job_DataSchemaChanged"
        return self.job_log(params)

    @log_method
    def data_schema_has_changed_with_reason(self, params, backup_type, reason_text, database):
        params["ActionType"] = "Job_ChangeBackupType3"
        params["LogParams"] = {'BackupType':backup_type, 
         'Error':reason_text, 
         'Database':database}
        return self.job_log(params)

    @log_method
    def restore_responce(self, params, message):
        params["ActionType"] = "Job_ScriptAfterRestore1"
        params["LogParams"] = {"Message": message}
        return self.job_log(params)

    def create_azure_snapshot(self, params, source_database, snapshot_name):
        params["ActionType"] = "Sql_CreateSnapshotDatabase1"
        params["LogParams"] = {'Database':source_database, 
         'SnapshotName':snapshot_name}
        return self.job_log(params)

    def export_azure_database(self, params, database_name, backup_extension):
        params["ActionType"] = "Sql_BackupDatabaseBacpac2"
        params["LogParams"] = {'Database':database_name, 
         'Ext':backup_extension}
        return self.job_log(params)

    def drop_azure_snapshot(self, params, snapshot_name):
        params["ActionType"] = "Sql_DropSnapshotDatabase1"
        params["LogParams"] = {"SnapshotName": snapshot_name}
        return self.job_log(params)

    @log_method
    def push_logs_to_server(self, backup_id, job_mode):
        remoute_backup_id = None
        while True:
            logs = self.get_unsent_backup_log_records(backup_id, job_mode)
            if logs is None:
                break
            res = self.push_unsent_logs_to_server(logs)
            remoute_backup_id = self.update_backup_remote_id(res)

        return remoute_backup_id

    def try_sync_log_with_serverParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def sql_binlog_backuped(self, params, file, size):
        params["ActionType"] = "Sql_BinLogBackuped2"
        params["LogParams"] = {'File':file, 
         'Size':size}
        return self.job_log(params)

    @log_method
    def skip_backup_database(self, params, db_name, message):
        params["ActionType"] = "Job_SkipDatabaseBackup2"
        params["LogParams"] = {'Database':db_name, 
         'Warning':message}
        return self.job_log(params)
