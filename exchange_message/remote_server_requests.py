
import urllib.parse, requests, time, os, sqlbak.config.agent_settings
from sqlbak.definitions import CONFIG, TIMEOUT, TRIGGER_BACKUP_TYPES, BACKUP_JOB_MODE
from sqlbak.helper import Helper
from sqlbak.logger import log_data, log_method, log_without_raising, log_only_exception
from requests.exceptions import ConnectionError

class RemoteServerRequest:

    def __init__(self):
        self.helper = Helper()
        self.web_api_protocol = "https://api"
        if os.path.exists(CONFIG["PATH_TO_APP"] + CONFIG["WEB_API_PATH"]):
            with open(CONFIG["PATH_TO_APP"] + CONFIG["WEB_API_PATH"], "r") as f:
                self.web_api_protocol = f.read().strip()
        self.web_api_path = self.web_api_protocol + ".sqlbak.com/"
        api_root = self.web_api_path + "Client/Service/"
        rest_var = "/rest/"
        self.listener_service_url = api_root + "Listener.svc" + rest_var
        self.agent_service_url = api_root + "AccountContent.svc" + rest_var
        self.backup_service_url = api_root + "BackupLog.svc" + rest_var
        self.client_service_url = api_root + "ClientContent.svc" + rest_var
        self.client_trace_service_url = api_root + "ClientTrace.svc" + rest_var
        self.download_trace_service_url = api_root + "DownloadTrace.svc" + rest_var
        self.job_trace_service_url = api_root + "JobTrace.svc" + rest_var
        self.logger_service_url = api_root + "Logging.svc" + rest_var
        self.monitoring_database_service_url = api_root + "MonitoringDataBase.svc" + rest_var
        self.monitoring_folder_service_url = api_root + "MonitoringFolder.svc" + rest_var
        self.oauth2_service_url = api_root + "OAuth2.svc" + rest_var
        self.quick_listener_service_url = api_root + "QuickListener.svc" + rest_var
        self.receiver_service_url = api_root + "Receiver.svc" + rest_var
        self.restore_trace_service_url = api_root + "RestoreTrace.svc" + rest_var
        self.sender_service_url = api_root + "Sender.svc" + rest_var
        self.logger_url = api_root + "Logging.svc" + rest_var

    @log_only_exception
    def make_requestParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_only_exception
    def request_wrapper(self, params=None, attempts=4, time_out=TIMEOUT, sleep_between_attempts=1):
        """
        A method is a wrapper to make a request to a remote server
        :param params:
        :param attempts:
        :param time_out:
        :return:
        """
        return self.helper.run_method_with_number_attempts_and_timeout(RemoteServerRequest, "make_request", params=(params,), attempts=attempts, time_out=(2 * TIMEOUT), sleep_between_attempts=sleep_between_attempts)

    @log_only_exception
    def confirm_agent_messages(self, agent_key, agent_id, has_messages, date_time, request_parameters):
        url = self.listener_service_url + "ConfirmCheck?agentKey=" + str(agent_key)
        is_get_request = False
        if request_parameters is None:
            data = {'AgentId':int(agent_id),  'HasMessages':bool(has_messages), 
             'RequestParameters':None, 
             'CreatedDateUtc':date_time, 
             'RequestTag':"test"}
        else:
            data = {'AgentId':int(agent_id),  'HasMessages':bool(has_messages), 
             'RequestParameters':{'CheckInterval':int(request_parameters["CheckInterval"]), 
              'CheckDuration':int(request_parameters["CheckDuration"])}, 
             'CreatedDateUtc':date_time, 
             'RequestTag':"test"}
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def register_agent(self, secret_key, agent_name, utils_path, client_version, session_id):
        url = self.agent_service_url + "RegisterAgent?secretKey=" + secret_key + "&agentName=" + str(agent_name)
        is_get_request = False
        data = {'MajorVersion':client_version["major_version"], 
         'MinorVersion':client_version["minor_version"], 
         'PatchVersion':client_version["patch_version"], 
         'ApplicationType':2, 
         'Settings':{"Paths": utils_path}, 
         'SystemInfo':(self.helper.get_user_machine_info_in_xml)(), 
         'SessionId':session_id}
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def update_agent_name(self, agent_key, agent_id, agent_name):
        url = self.agent_service_url + "UpdateAgentSettings?agentKey=" + agent_key
        is_get_request = False
        data = {'AgentId':str(agent_id), 
         'AgentName':agent_name}
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def get_agent_status(self, agent_key):
        url = self.agent_service_url + "Get?agentKey=" + agent_key
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_agent_info(self, secret_key, agent_key):
        url = self.agent_service_url + "GetEx?secretKey=" + secret_key + "&agentKey=" + agent_key
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def update_agent(self, agent, utils_path):
        url = self.agent_service_url + "UpdateAgent?agentKey=" + str(agent["AgentKey"])
        is_get_request = False
        data = {'MajorVersion':int(agent["MajorVersion"]), 
         'MinorVersion':int(agent["MinorVersion"]), 
         'PatchVersion':int(agent["PatchVersion"]), 
         'Settings':{"Paths": utils_path}, 
         'SystemInfo':(self.helper.get_user_machine_info_in_xml)(), 
         'SessionId':agent["SessionId"]}
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def set_agent_activity(self, agent_key, do_activate):
        url = self.agent_service_url + "SetIsActive?agentKey=" + agent_key + "&isActive=" + str(do_activate)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_backups_for_restore(self, agent_key, backup_object_id, destination_id):
        url = self.backup_service_url + "GetBackupsForRestoreEx?agentKey=" + str(agent_key) + "&backupObjectId=" + str(backup_object_id) + "&destinationId=" + str(destination_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_backup_object_info(self, backup_object_id):
        url = self.backup_service_url + "GetBackupObjectInfo?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key()) + "&backupObjectId=" + str(backup_object_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def save_job_credentials(self, agent_key, server_type, name, version, job_credential_id):
        data = {
         'JobCredentialsId': job_credential_id, 
         'Name': name, 
         'Version': version, 
         'JobIds': None, 
         'ServerType': server_type}
        url = self.client_service_url + "SaveJobCredentials?agentKey=" + agent_key
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def delete_job_credentials(self, agent_key, connection_id):
        url = self.client_service_url + "DeleteJobCredentials?agentKey=" + str(agent_key) + "&connectionId=" + str(connection_id)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def trace_begin_job(self, params):
        data = {'MessageId':int(params["MessageId"]) if (params["MessageId"] is not None) else (params["MessageId"]), 
         'JobId':int(params["JobId"]), 
         'BackupType':(params["BackupType"][0[:1]].lower)(), 
         'BeginAt':("/Date({0})/".format)(self.helper.get_time_in_milliseconds()), 
         'BackupKey':str(params["BackupKey"]), 
         'Mode':str(params["JobMode"]), 
         'JobCredentialsId':params["JobCredentialsId"], 
         'IsEncrypted':params["IsEncryptionEnabled"]}
        url = self.job_trace_service_url + "BeginJob?agentKey=" + str(params["AgentKey"])
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_end_job(self, params, backup):
        if "FailureMailConditionInterval" in params:
            split_interval = str(params["FailureMailConditionInterval"]).split(":")
            interval = str("PT{0}H{1}M{2}S".format(int(split_interval[0]), int(split_interval[1]), int(split_interval[2])))
        else:
            interval = None
        data = {'JobId':int(params["JobId"]), 
         'BackupId':int(params["BackupRemoteId"]) if ("BackupRemoteId" in params and params["BackupRemoteId"] is not None) else (backup["RemoteId"]), 
         'IsSuccess':int(params["CountJobErrors"]) == 0, 
         'Status':1 if (int(params["CountJobErrors"]) == 0) else 3, 
         'Size':int(params["GeneralSize"]) if ("GeneralSize" in params) else 0, 
         'ArchiveSize':int(params["GeneralArchiveSize"]) if ("GeneralArchiveSize" in params) else 0, 
         'EndAt':("/Date({0})/".format)(self.helper.get_time_in_milliseconds()), 
         'MailLogInfo':{'Enabled':(self.is_email_enabled)(params, backup["BackupType"]), 
          'SmtpInfo':{'MailTo':params["SuccessMailAddressTo"] if (int(params["CountJobErrors"]) == 0) else (params["FailureMailAddressTo"]), 
           'MailFrom':""}, 
          'ServiceName':"", 
          'FailureMailCondition':{'Enabled':bool(params["FailureMailConditionEnable"]), 
           'FailureCount':None, 
           'Interval':interval}}, 
         'NextScheduledBackup2':{'JobId':int(params["JobId"]), 
          'BackupTime':None, 
          'BackupType':None}}
        url = self.job_trace_service_url + "EndJob?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        log_data(url)
        log_data(data)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data), sleep_between_attempts=15)

    @log_method
    def trace_failed_job(self, job_id, failure_mail, message_id, error_str):
        url_begin = self.job_trace_service_url + "BeginJob?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        url_append = self.job_trace_service_url + "AppendLogRecords?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        url_end = self.job_trace_service_url + "EndJob?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        current_time = self.helper.get_time_in_milliseconds()
        data_begin = {'MessageId':message_id, 
         'JobId':job_id, 
         'BackupType':"f", 
         'BeginAt':f"/Date({current_time})/", 
         'BackupKey':(self.helper.get_uuid)(), 
         'Mode':1, 
         'JobCredentialsId':0, 
         'IsEncrypted':None}
        begin_job_result = self.request_wrapper(params=(False, url_begin, data_begin))
        if not begin_job_result["IsSuccess"]:
            raise Exception("Failed to trace begin job")
        backup_id = begin_job_result["Data"]["BackupId"]
        current_time = self.helper.get_time_in_milliseconds()
        data_append = {'BackupId':backup_id, 
         'BackupLogRecords':[
          {'ActionType':"Job_RunError1", 
           'CreatedTime':f"/Date({current_time})/", 
           'Severity':4, 
           'BackupLogKey':(self.helper.get_uuid)(), 
           'BackupLogParamRecords':[
            {'ParamName':"Error", 
             'ParamValue':str(error_str)}]}]}
        trace_log_error_result = self.request_wrapper(params=(False, url_append, data_append))
        current_time = trace_log_error_result["IsSuccess"] or self.helper.get_time_in_milliseconds()
        data_end = {'JobId':job_id, 
         'BackupId':backup_id, 
         'IsSuccess':False, 
         'Status':3, 
         'Size':0, 
         'ArchiveSize':0, 
         'EndAt':f"/Date({current_time})/", 
         'MailLogInfo':{'Enabled':True, 
          'SmtpInfo':{'MailTo':failure_mail, 
           'MailFrom':""}, 
          'ServiceName':"", 
          'FailureMailCondition':{'Enabled':True, 
           'FailureCount':None, 
           'Interval':"PT0H5M0S"}}, 
         'NextScheduledBackup2':{'JobId':job_id, 
          'BackupTime':None, 
          'BackupType':None}}
        result = self.request_wrapper(params=(False, url_end, data_end))
        if not result["IsSuccess"]:
            raise Exception("Failed to trace failed end job")

    @log_method
    def is_email_enabled(self, params, backup_type):
        is_backup_type_enabled = False
        if bool(params["EmailInfoEnabled"]):
            log_data("Email enabled")
            if "SuccessBackupTypes" in params:
                log_data("SuccessBackupTypes exist")
                for p in params["SuccessBackupTypes"]:
                    log_data("SuccessBackupTypes-item: {}, params-BackupType: {}".format(p, backup_type))

                if p in TRIGGER_BACKUP_TYPES and TRIGGER_BACKUP_TYPES[p] == backup_type:
                    is_backup_type_enabled = True
                    break
            else:
                is_backup_type_enabled = True
        return is_backup_type_enabled

    @log_only_exception
    def trace_backup_object(self, params, agent_key):
        url = self.job_trace_service_url + "TraceBackupObject?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, params))

    @log_method
    def trace_backup_log(self, params):
        data = {'BackupId':int(params["BackupRemoteId"]), 
         'ActionType':params["ActionType"], 
         'Parameters':[
          params["LogParams"]], 
         'CreatedAt':("/Date({0})/".format)(self.helper.get_time_in_milliseconds()), 
         'Severity':int(params["Severity"]), 
         'BackupLogKey':str(params["BackupLogKey"])}
        url = self.job_trace_service_url + "TraceBackupLog?agentKey=" + str(params["AgentKey"])
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_backup_logs(self, agent_key):
        url = self.job_trace_service_url + "TraceBackupLogs?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def trace_backup_object_result(self, params, agent_key):
        url = self.job_trace_service_url + "TraceBackupObjectResult?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, params))

    @log_method
    def get_backup_items(self, agent_key):
        url = self.job_trace_service_url + "GetBackupItems?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_backup_item(self, agent_key):
        url = self.job_trace_service_url + "GetBackupItem?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def upload_job_backup_x(self, xml_string):
        url = self.job_trace_service_url + "UploadJobBackupX?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url,
         {"backupRecord": (str(xml_string))}))

    @log_method
    def append_log_records(self, params):
        agent_key, log_params = params
        url = self.job_trace_service_url + "AppendLogRecords?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, log_params))

    @log_method
    def validate_emails(self, agent_key):
        url = self.job_trace_service_url + "ValidateEmails?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_token_info(self, agent_key, destination_id):
        url = self.oauth2_service_url + "GetTokenInfo?agentKey=" + str(agent_key) + "&destinationId=" + str(destination_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_only_exception
    def quick_listener_check(self, agent_key, session_id):
        request_tag = "test"
        url = self.quick_listener_service_url + "Check3?agentKey=" + str(agent_key) + "&requestTag=" + request_tag + "&sessionId=" + session_id
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_only_exception
    def get_simple_receiver(self, agent_key):
        request_tag = "test"
        data = {'AgentKey':agent_key, 
         'IsToServer':True}
        url = self.receiver_service_url + "GetSimple?requestTag=" + request_tag
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def send_message(self, agent_key, message, receiver_id=None):
        data = {'MessageId':message["MessageId"], 
         'MessageType':int(message["MessageType"]), 
         'AgentKey':str(agent_key), 
         'ReceiverId':receiver_id, 
         'IsToServer':message["IsToServer"] if ("IsToServer" in message) else True, 
         'Data':message["MessageData"], 
         'IsResponseExpected':message["IsResponseExpected"] if ("IsResponseExpected" in message) else False, 
         'CreatedDateUtc':None}
        url = self.sender_service_url + "SendMessage?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def send_messages(self, agent_key):
        url = self.sender_service_url + "SendMessages?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def cancel_message(self, agent_key, message_id):
        url = self.sender_service_url + "CancelMessage?agentKey=" + str(agent_key) + "&messageId=" + str(message_id) + "&cancelProcess=True"
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def get_job_plan_violation(self, job_id):
        url = self.job_trace_service_url + "GetJobPlanViolations?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key()) + "&jobId=" + str(job_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def upload_file_chunk(self, agent_key, session_id, file_name, file_content):
        data = {'SessionId':str(session_id), 
         'FileName':str(file_name), 
         'ChunkContent':list(file_content)}
        url = self.logger_url + "UploadFileChunk?agentKey=" + str(agent_key)
        is_get_request = False
        result = self.request_wrapper(params=(is_get_request, url, data))
        return result

    @log_method
    def send_log_to_developers(self, agent_key, session_id):
        data = {"SessionId": (str(session_id))}
        url = self.logger_url + "SendLogToDevelopers?agentKey=" + str(agent_key)
        return self.request_wrapper(params=(False, url, data))

    @log_method
    def check_update_status(self, agent_key, mode):
        data = {"Mode": mode}
        url = self.agent_service_url + "CheckUpdateStatus2?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_begin_restore(self, agent_key, message_id, object_id, object_name, restore_status, message, job_credential_id):
        url = self.restore_trace_service_url + "BeginRestore?agentKey=" + str(agent_key)
        data = {'MessageId':message_id, 
         'BackupObjectId':object_id, 
         'ConnectionInfo':"", 
         'ObjectName':object_name, 
         'Status':restore_status, 
         'Message':message, 
         'StartTime':str("/Date({0})/".format(self.helper.get_time_in_milliseconds())), 
         'Backups':[
          {
           'BackupObjectId': object_id, 
           'DownloadId': None, 
           'Status': 0, 
           'Message': None}], 
         'JobCredentialsId':job_credential_id}
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_restore(self, agent_key, restore_id, object_id, restore_status, download_status, message, download_message, date_time):
        url = self.restore_trace_service_url + "TraceRestore?agentKey=" + str(agent_key)
        data = {'RestoreId':restore_id, 
         'BackupObjectId':object_id, 
         'Status':restore_status, 
         'Message':message, 
         'EndTime':date_time, 
         'Backups':[
          {
           'BackupObjectId': object_id, 
           'DownloadId': None, 
           'Status': download_status, 
           'Message': download_message}]}
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_end_restore(self, agent_key, restore_id, object_id, restore_status, download_status, message, download_message):
        url = self.restore_trace_service_url + "EndRestore?agentKey=" + str(agent_key)
        data = {'RestoreId':restore_id, 
         'BackupObjectId':object_id, 
         'Status':restore_status, 
         'Message':message, 
         'EndTime':str("/Date({0})/".format(self.helper.get_time_in_milliseconds())), 
         'Backups':[
          {
           'BackupObjectId': object_id, 
           'DownloadId': None, 
           'Status': download_status, 
           'Message': download_message}]}
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def begin_download(self, message_id, object_id, work_dir, size, start_time):
        data = {'MessageId':int(message_id), 
         'BackupObjectId':int(object_id), 
         'WorkingDir':str(work_dir), 
         'TotalSize':int(size), 
         'StartTime':start_time}
        url = self.download_trace_service_url + "BeginDownload?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def end_download(self, agent_key, download_id, object_id, status, progress_size, total_size, end_time):
        data = {'BackupObjectId':int(object_id), 
         'DownloadId':int(download_id), 
         'Status':int(status), 
         'EndTime':end_time, 
         'ProgressSize':progress_size, 
         'TotalSize':total_size}
        url = self.download_trace_service_url + "EndDownload?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def begin_file_download(self, agent_key, download_id, object_id, total_size, start_time):
        data = {'BackupObjectFileId':int(object_id), 
         'DownloadId':int(download_id), 
         'StartTime':start_time, 
         'TotalSize':int(total_size)}
        url = self.download_trace_service_url + "BeginFileDownload?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def trace_download(self, agent_key, download_id, object_id, object_file_id, total_size, progress_size):
        data = {'BackupObjectId':int(object_id), 
         'DownloadId':int(download_id), 
         'TotalSize':int(total_size), 
         'ProgressSize':"", 
         'Files':[
          {'BackupObjectFileId':int(object_file_id), 
           'TotalSize':int(total_size), 
           'ProgressSize':int(progress_size)}]}
        url = self.download_trace_service_url + "TraceDownload?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def end_file_download(self, agent_key, download_id, object_id, progress_size, total_size, status, message, end_time):
        data = {'BackupObjectFileId':int(object_id), 
         'DownloadId':int(download_id), 
         'Status':int(status), 
         'EndTime':end_time, 
         'ProgressSize':int(progress_size), 
         'TotalSize':int(total_size), 
         'Message':str(message)}
        url = self.download_trace_service_url + "EndFileDownload?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_only_exception
    def get_backups_for_cleanup(self, data):
        url = self.backup_service_url + "GetBackupsForCleanup?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key())
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data), attempts=6, time_out=TIMEOUT, sleep_between_attempts=5)

    @log_method
    def get_backup_job_info(self, agent_key, backup_object_id):
        url = self.backup_service_url + "GetBackupJobInfo?agentKey=" + str(agent_key) + "&backupObjectId=" + str(backup_object_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def trace_client_event(self, agent_key, data):
        url = self.client_trace_service_url + "TraceEvent?agentKey=" + str(agent_key)
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def remove_backup_files_list(self, backup_object_ids):
        url = self.backup_service_url + "DeleteBackupFilesList?agentKey=" + str(sqlbak.config.agent_settings.get_agent_key()) + "&pageSize=0"
        is_get_request = False
        return self.request_wrapper(params=(is_get_request, url, backup_object_ids))

    @log_only_exception
    def get_message(self, agent_key, message_id):
        url = self.receiver_service_url + "GetMessage?agentKey={0}&messageId={1}".format(agent_key, urllib.parse.quote(message_id))
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_only_exception
    def get_info_by_message(self, agent_key, message_id):
        url = self.restore_trace_service_url + "GetInfoByMessage?agentKey={0}&messageId={1}".format(agent_key, message_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def notify_about_dbms_connection(self, agent_key, connections):
        url = self.monitoring_database_service_url + "NotifyAboutBadConnectionWithDbms?agentKey={0}".format(agent_key)
        is_get_request = False
        data = []
        for connection in connections:
            data.append({'StateActivityDbms':connection["activity"], 
             'ServerName':connection["server_name"], 
             'StateDate':str("/Date({0})/".format(int(time.mktime(connection["state_date"].timetuple()) * 1000))), 
             'TimePreviosStateChange':str("/Date({0})/".format(int(time.mktime(connection["previous_date"].timetuple()) * 1000))), 
             'ServerType':connection["server_type"], 
             'ErrorDetail':connection["error"]})
        else:
            return self.request_wrapper(params=(is_get_request, url, data))

    @log_without_raising
    def trace_application_event(self, data):
        url = self.client_trace_service_url + "TraceApplicationEvent"
        is_get_request = False
        self.request_wrapper(params=(is_get_request, url, data))

    @log_method
    def get_short(self, agent_key, agent_id):
        url = self.agent_service_url + "GetShort?agentKey={0}&agentId={1}".format(agent_key, agent_id)
        is_get_request = True
        return self.request_wrapper(params=(is_get_request, url))

    @log_method
    def ping_restore(self, agent_key, restore_id):
        url = self.restore_trace_service_url + "PingRestore?agentKey={0}".format(agent_key)
        is_get_request = False
        data = {'RestoreId':int(restore_id), 
         'PingAt':str("/Date({0})/".format(self.helper.get_time_in_milliseconds()))}
        self.request_wrapper(params=(is_get_request, url, data))


remoute_server_request_instanse = RemoteServerRequest()
# NOTE: have internal decompilation grammar errors.
# Use -T option to show full context.
# not in loop:
#	break (2)
#      0.  L. 357        92  POP_TOP          
#      1.                94  BREAK_LOOP          104  'to 104'
