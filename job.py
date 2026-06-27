from logging import exception
import os
from sqlbak.exchange_message.helper import IsIntensiveMode
import sqlbak.config.agent_settings
from sqlbak.definitions import BACKUP_TYPES, SEVERITY_PARAMS, PROCESS_TYPES, CONFIG, BACKUP_JOB_MODE, SUDO_SQLBAK
from sqlbak.helper import Helper
from sqlbak.job_log import JobLog
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.job_settings import JobSettings
from sqlbak.trace_event import TraceEvent
from sqlbak.logger import log_error, log_method, log_without_raising, log_only_exception
from sqlbak.app_output import APP_OUTPUT

class Job:

    def __init__(self):
        self.local_db = LocalDB()
        self.job_log = JobLog()
        self.remote_request = RemoteServerRequest()
        self.count_job_errors = 0
        self.params = {}
        self.helper = Helper()
        self.job_settings = JobSettings()
        self.trace_event = TraceEvent()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def set_job_settings(self):
        self.params.update(self.job_settings.get_job_settings(self.params))

    @log_method
    def get_initial_settings(self, params):
        self.params = self.job_settings.get_initial_job_settings(params)

    @log_method
    def callback(self, job_params):
        if "SendMessage" in job_params:
            if job_params["SendMessage"] is not None:
                callback = job_params["SendMessage"]
                callback(job_params["Message"], {'IsSuccess':True, 
                 'Message':"", 
                 'Error':None})

    @log_method
    def begin_job(self):
        if not IsIntensiveMode():
            if not self.params["IsSilentMode"]:
                try:
                    self.params["BackupRemoteId"] = self.trace_begin_job()
                    self.local_db.update_process(os.getpid(), self.params["JobId"], self.params["BackupRemoteId"])
                    self.local_db.update_backup_remote_id(self.params["BackupId"], self.params["BackupRemoteId"])
                except Exception as e:
                    try:
                        log_error(e, "Can't get remote id")
                        self.local_db.update_process(os.getpid(), self.params["JobId"], self.params["BackupId"])
                        self.params["BackupRemoteId"] = None
                    finally:
                        e = None
                        del e

        else:
            self.params["BackupRemoteId"] = None
            self.local_db.update_process(os.getpid(), self.params["JobId"], self.params["BackupId"])

    @log_method
    def trace_begin_job(self):
        res = self.remote_request.trace_begin_job(self.params)
        if not res["IsSuccess"]:
            raise Exception(res["ErrorMessage"])
        return res["Data"]["BackupId"]

    @log_method
    def catch_job_error(self, error):
        """

        :param error:
        :return:
        """
        self.params["CountJobErrors"] += 1
        self.params["Severity"] = SEVERITY_PARAMS["Error"]
        self.params = self.job_log.send_error_log(self.params, self.helper.get_knowledge_base_error(error, True))
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def catch_job_warning(self, warning):
        self.params["Severity"] = SEVERITY_PARAMS["Warning"]
        self.params = self.job_log.send_error_log(self.params, self.helper.get_knowledge_base_error(warning, True))
        self.params["Severity"] = SEVERITY_PARAMS["Info"]

    @log_method
    def cleanup_backup_job_logs(self):
        self.local_db.delete_backup_log_and_param_by_backup_id_forced(self.params["BackupId"], [
         'Job_ChangeBackupType2', 
         'Job_ChangeBackupType3', 
         'Job_ChangeBackupType4', 
         'Job_ScheduledStart3', 
         'Job_ScheduledStart4', 
         'Job_ScheduledStart5', 
         'Job_Start3', 
         'Job_Start4', 
         'Job_Start5', 
         'Job_CliStart5', 
         'Job_FinishedSuccessfully1'])

    @log_method
    def send_unsend_backup_logs(self, backup_id, job_mode):
        try:
            remote_id = self.job_log.try_sync_log_with_server(backup_id, job_mode)
            if remote_id:
                self.job_log.params["BackupRemoteId"] = remote_id
                self.params["BackupRemoteId"] = remote_id
        except Exception as e:
            try:
                self.catch_job_error(e)
            finally:
                e = None
                del e

    @log_method
    def end_job(self, params=None):
        if params is not None:
            self.params = params
        else:
            self.local_db.end_backup(self.params["BackupId"], int(self.params["CountJobErrors"]) == 0)
            self.local_db.delete_process_by_main_id(self.params["BackupId"], PROCESS_TYPES["BACKUP"])
            if "BackupRemoteId" in self.job_log.params:
                if self.job_log.params["BackupRemoteId"]:
                    self.local_db.delete_process_by_main_id(self.params["BackupRemoteId"], PROCESS_TYPES["BACKUP"])
            backup = self.local_db.get_backup_by_id(self.params["BackupId"])
            res = self.remote_request.trace_end_job(self.params, backup)
            assert res["IsSuccess"], str(res["ErrorMessage"])
        self.local_db.clean_backup_logs(self.params["BackupId"])

    @log_method
    def cancel_job(self, remote_backup_id):
        """

        :param agent_key:
        :param remote_backup_id:
        :return:
        """
        backup_job = self.local_db.get_backup_and_job_by_backup_remote_id(remote_backup_id)
        if backup_job is None:
            raise Exception(self.cm["BACKUP_NOT_FOUND"].format(str(remote_backup_id)))
        self.stop_job_processes(remote_backup_id)
        self.local_db.delete_process_by_main_id(remote_backup_id, PROCESS_TYPES["BACKUP"])
        self.log_cancel_job(remote_backup_id, backup_job["Id"])
        email_settings = self.job_settings.get_job_email_settings(backup_job)
        self.send_unsend_backup_logs(backup_job["Id"], BACKUP_JOB_MODE["MANUAL"])
        self.end_job({'IsSilentMode':False, 
         'BackupId':backup_job["Id"], 
         'AgentKey':(sqlbak.config.agent_settings.get_agent_key)(), 
         'CountJobErrors':1, 
         'Status':3, 
         'JobId':backup_job["JobId"], 
         'BackupRemoteId':remote_backup_id, 
         'Size':backup_job["Size"], 
         'ArchiveSize':backup_job["ArchiveSize"], 
         'JobMode':BACKUP_JOB_MODE["MANUAL"], 
         'SuccessMailAddressTo':email_settings["SuccessMailAddressTo"], 
         'EmailInfoEnabled':email_settings["EmailInfoEnabled"], 
         'FailureMailAddressTo':email_settings["FailureMailAddressTo"], 
         'FailureMailConditionEnable':email_settings["FailureMailConditionEnable"]})

    @log_method
    def stop_job_processes(self, backup_id):
        job_processes = self.local_db.get_process_by_main_id(backup_id, PROCESS_TYPES["BACKUP"])
        for process in job_processes:
            self.stop_job_process(process["Pid"])

    @log_without_raising
    def stop_job_process(self, pid):
        if not self.helper.stop_process_and_return_is_success(pid):
            raise Exception("Job with process id {0} was not stopped".format(pid))

    @log_method
    def log_cancel_job(self, remote_backup_id, backup_id):
        self.params = {'IsConsoleMode':False, 
         'IsSilentMode':True, 
         'BackupRemoteId':remote_backup_id, 
         'Severity':SEVERITY_PARAMS["Error"], 
         'AgentKey':(sqlbak.config.agent_settings.get_agent_key)(), 
         'BackupId':backup_id}
        self.params = self.job_log.cancel_job(self.params, self.cm["CANCEL_JOB"])

    @log_method
    def set_object_backup_result(self):
        for backup in self.params["ObjectBackupResults"]:
            try:
                object_result = self.local_db.get_object_backup_result(backup["object_name"], self.params["JobId"], backup["object_type"])
                is_success = self.is_backup_result_success()
                if object_result is None:
                    backup_type = self.get_backup_type(backup["object_type"])
                    object_result_id = self.local_db.add_object_backup_result(backup["object_name"], is_success, self.params["JobId"], backup_type, backup["object_type"], self.params["BackupId"], self.params["BackupAt"], self.params["ServerType"])
                else:
                    object_result_id = object_result["ObjectBackupResultId"]
                    self.local_db.update_object_backup_result(object_result_id, is_success, self.params["BackupAt"], self.params["ServerType"], self.params["BackupId"])
                for destination in backup["destinations"]:
                    self.set_object_destination_result(object_result_id, destination["settings"]["DestinationId"], int(destination["is_success"]))
                else:
                    if is_success:
                        if backup["object_type"] == BACKUP_TYPES["FULL"]:
                            self.local_db.set_all_backup_types_success_for_job_id(backup["object_name"], self.params["JobId"])

            except Exception as e:
                try:
                    self.catch_job_error(self.cm["FAILED_UPDATE_OBJECT"].format(str(e)))
                finally:
                    e = None
                    del e

    @log_method
    def get_backup_type(self, object_type):
        res = self.helper.get_backup_type_by_object_type(object_type)
        if res is None:
            raise Exception(self.cm["INVALID_BACKUP_TYPE"].format(str(object_type)))
        return res[0[:1]].lower()

    @log_method
    def is_backup_result_success(self):
        return int(self.params["CountJobErrors"]) == 0

    @log_only_exception
    def set_object_destination_result(self, object_result_id, destination_id, is_success):
        if self.local_db.get_object_destination_result(object_result_id, destination_id) is None:
            self.local_db.add_object_destination_result(object_result_id, destination_id, is_success)
        else:
            self.local_db.reset_object_destination_result(object_result_id, destination_id, is_success)

    @log_method
    def get_backup_settings(self, backup, agent_key):
        job = self.local_db.get_job_by_id(backup["JobId"])
        email_settings = self.job_settings.get_job_email_settings(job)
        return {'IsSilentMode':True, 
         'BackupId':backup["Id"], 
         'AgentKey':agent_key, 
         'CountJobErrors':1, 
         'Status':3, 
         'JobId':backup["JobId"], 
         'BackupRemoteId':backup["RemoteId"], 
         'Size':backup["Size"], 
         'ArchiveSize':backup["ArchiveSize"], 
         'JobMode':BACKUP_JOB_MODE["SCHEDULE"], 
         'SuccessMailAddressTo':email_settings["SuccessMailAddressTo"], 
         'EmailInfoEnabled':email_settings["EmailInfoEnabled"], 
         'FailureMailAddressTo':email_settings["FailureMailAddressTo"], 
         'FailureMailConditionEnable':email_settings["FailureMailConditionEnable"]}

    @log_method
    def reset_object_backup_result(self):
        for db_name in self.params["Databases"]:
            object_type = BACKUP_TYPES[self.params["BackupType"]]
            object_result = self.local_db.get_object_backup_result(db_name, self.params["JobId"], object_type)
            if object_result is not None:
                self.local_db.reset_object_backup_result(object_result["ObjectBackupResultId"], 0)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/job.pyc
