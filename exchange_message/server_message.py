import json, os
from datetime import datetime, timedelta
from operator import itemgetter
from sqlbak.helpers.permissons import reset_access_for_working_dir
import sqlbak.config.agent_settings
from sqlbak.job_operation.restore import handle_restore_message
from sqlbak.trace_event import TraceEvent
import time
from sqlbak.definitions import DOWNLOAD_STATUSES, BACKUP_TYPES, DESTINATIONS_WITH_ACCESS_TOKEN, BACKUP_JOB_MODE, MSSQL_CONST
from sqlbak.definitions import MESSAGE_TYPES_CONSTS, SYNCHRONOUS_MESSAGE_TYPES, FULL_BACKUP_CONST, DESTINATIONS_CONSTS, DBMS_TYPES_CONSTS
from sqlbak.definitions import UPDATE_APP_SOURCES, RESTORE_STATUSES, PROCESS_TYPES, ZIP_EXT, CONFIG, DYNAMIC_SETTING_LOGGING_ACTIVATED, SEC_IN_MILLISECOND, MINUTE_IN_SEC
from sqlbak.destinations.destination import Destination
from sqlbak.helper import Helper
from sqlbak.job import Job
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.dbms.dbms import DBMS
from sqlbak.plain_job import PlainJob
from sqlbak.update import UpdateApp
from sqlbak.restore import Restore
from sqlbak.download import Download
from sqlbak.upload import UploadAppLogs
from sqlbak.logger import log_method, log_without_raising, log_only_exception, log_data
from sqlbak.exceptions import UnregisterAgent
from sqlbak.app_output import APP_OUTPUT
from sqlbak.connection import Connection
from sqlbak.process_managment.helper import set_subservice_title
from sqlbak.helpers.temporary_directory import create_directory

class ServerMessage:

    def __init__(self):
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.plain_job = PlainJob()
        self.helper = Helper()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.connection = Connection()

    @log_only_exception
    def pin_remote_serverParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_only_exception
    def get_remote_data(self):
        res = self.remote_request.quick_listener_checksqlbak.config.agent_settings.get_agent_keysqlbak.config.agent_settings.session_id
        if "IsConnectionError" in res:
            if res["IsConnectionError"]:
                log_data(res["ErrorMessage"])
                time.sleep20
                return
        if not res["IsSuccess"]:
            self.local_db.remove_request_params
            raise Exception(str(res["ErrorMessage"]))
        return res["Data"]

    @log_only_exception
    def get_remote_messages(self):
        res = self.remote_request.get_simple_receiversqlbak.config.agent_settings.get_agent_key
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        if res["Data"] is None or "Messages" not in res["Data"]:
            raise Exception(self.cm["FAILED_RECEIVE_MESSAGES"].formatstr(res["Data"]))
        return res["Data"]["Messages"]

    @log_method
    def handle_server_messages(self, messages):
        """
        A method to handle a remote server messages
        :param messages: dict
        :return: None
        """
        set_subservice_title("server-messages")
        for message in sorted(messages, key=(itemgetter("CreatedDateUtc"))):
            if not self.local_db.does_message_existsmessage["MessageId"]:
                self.local_db.add_messagemessage["MessageId"]
                if message["MessageType"] not in SYNCHRONOUS_MESSAGE_TYPES:
                    process = self.helper.run_additional_processself.handle_messagemessage
                    process.join0
                else:
                    self.handle_messagemessage

    @log_without_raising
    def handle_message(self, message):
        """
        A method to handle a received message from a remote server
        :param message: dict
        :return: None
        """
        try:
            set_subservice_title("handle-message")
            message_handler = self.get_message_handler_by_message_typeint(message["MessageType"])
            message_params = self.get_message_paramsmessage
            message_handler(message_params)
        except Exception as e:
            try:
                self.mark_message_as_readmessage{'IsSuccess':False,  'Message':str(e),  'Error':None}
            finally:
                e = None
                del e

    @log_only_exception
    def get_message_params(self, message):
        message_params = {"MessageId": (message["MessageId"])}
        message_params.updatejson.loadsmessage["Data"]
        message_params.updatemessage
        return message_params

    @log_only_exception
    def mark_message_as_read(self, message, data):
        """
        Send a request to remote server to mark received message as read
        :param data: dict
        :param message: JSON object
        :return: None
        """
        agent = self.is_agent_active
        self.send_message_to_server(agent, message, data)

    def is_agent_active(self):
        agent = self.local_db.get_current_agent
        if agent is None or agent["IsActive"] != 1:
            self.local_db.remove_request_params
            raise UnregisterAgent
        return agent

    @log_method
    def send_message_to_server(self, agent, message, data):
        res = self.remote_request.send_messageagent["AgentKey"]{'MessageId':int(message["MessageId"]),  'MessageType':message["MessageType"], 
         'MessageData':(json.dumps)data, 
         'CreatedDateUtc':message["CreatedDateUtc"]}
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        else:
            self.local_db.end_messagemessage["MessageId"]

    @log_only_exception
    def save_duration_and_interval(self, params):
        duration = datetime.now + timedelta(seconds=(int(params["CheckDuration"]) / 1000))
        formated_date_time = duration.strftime"%Y-%m-%d %H:%M:%S.%f"
        self.local_db.save_request_paramsformated_date_timeparams["CheckInterval"]

    @log_only_exception
    def confirm_message(self, server_data, request_parameters):
        res = self.remote_request.confirm_agent_messages(sqlbak.config.agent_settings.get_agent_key, sqlbak.config.agent_settings.agent_id, server_data["HasMessages"], server_data["CreatedDateUtc"], request_parameters)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def get_message_handler_by_message_type(self, message_type):
        """
        Returns function-handler for a message according to a message type
        :param message_type: int
        :return: Function if function handler is found or None
        """
        messages_hub = {(MESSAGE_TYPES_CONSTS["SAVE_JOB"]): (self.save_job), 
         (MESSAGE_TYPES_CONSTS["DELETE_JOB"]): (self.delete_job), 
         (MESSAGE_TYPES_CONSTS["RUN_JOB"]): (self.run_job), 
         (MESSAGE_TYPES_CONSTS["CANCEL_JOB"]): (self.cancel_job), 
         (MESSAGE_TYPES_CONSTS["SAVE_DESTINATION"]): (self.save_destination), 
         (MESSAGE_TYPES_CONSTS["REQUEST_ENVIRONMENT"]): (self.save_credential_and_get_db_names), 
         (MESSAGE_TYPES_CONSTS["CHANGE_ACCOUNT_PLAN"]): (self.change_account_plan), 
         (MESSAGE_TYPES_CONSTS["TEST_DESTINATION"]): (self.test_destination), 
         (MESSAGE_TYPES_CONSTS["UPDATE_PROFILE"]): (self.update_user_profile), 
         (MESSAGE_TYPES_CONSTS["AGENT_CONFIGURATION_CHANGED"]): (self.update_agent_configuration), 
         (MESSAGE_TYPES_CONSTS["UPLOAD_LOGS"]): (self.upload_logs), 
         (MESSAGE_TYPES_CONSTS["ACTIVATE_LOGGING"]): (self.activate_logging), 
         (MESSAGE_TYPES_CONSTS["DEACTIVATE_LOGGING"]): (self.deactivate_logging), 
         (MESSAGE_TYPES_CONSTS["UPGRADE_APP"]): (self.upgrade_app), 
         (MESSAGE_TYPES_CONSTS["CHECK_TEMP_FOLDER"]): (self.check_temp_folder), 
         (MESSAGE_TYPES_CONSTS["RESTORE_BACKUP"]): (self.restore_backup), 
         (MESSAGE_TYPES_CONSTS["CANCEL_RESTORE_BACKUP"]): (self.cancel_restore_backup), 
         (MESSAGE_TYPES_CONSTS["DOWNLOAD_BACKUP"]): (self.download_backup), 
         (MESSAGE_TYPES_CONSTS["DOWNLOAD_FOLDER_BACKUP"]): (self.download_folder_backup), 
         (MESSAGE_TYPES_CONSTS["CANCEL_DOWNLOAD"]): (self.cancel_download), 
         (MESSAGE_TYPES_CONSTS["CANCEL_PROCESS"]): (self.cancel_process), 
         (MESSAGE_TYPES_CONSTS["SQL_SCRIPT_EXEC"]): (self.exec_sql_script), 
         (MESSAGE_TYPES_CONSTS["CHECK_DOWN_ALERT"]): (self.check_server_down_alert), 
         (MESSAGE_TYPES_CONSTS["DELETE_SERVER"]): (self.delete_server), 
         (MESSAGE_TYPES_CONSTS["RESTART_SERVICE"]): (self.restart_service), 
         (MESSAGE_TYPES_CONSTS["UPLOAD_DATABASE"]): (self.upload_local_db), 
         (MESSAGE_TYPES_CONSTS["EDIT_SERVER_NAME"]): (self.edit_server_name), 
         (MESSAGE_TYPES_CONSTS["GET_DBMS_CONNECTION_SETTINGS"]): (self.get_dbms_connection_settings), 
         (MESSAGE_TYPES_CONSTS["SAVE_DBMS_CONNECTION_SETTINGS"]): (self.save_dbms_connection_settings), 
         (MESSAGE_TYPES_CONSTS["DELETE_DBMS_CONNECTION_SETTINGS"]): (self.delete_dbms_connection_settings), 
         (MESSAGE_TYPES_CONSTS["TEST_DBMS_CONNECTION_SETTINGS"]): (self.test_dbms_connection)}
        if message_type in messages_hub:
            return messages_hub[message_type]
        raise Exception(self.cm["NO_MESSAGE_HANDLER"])

    @log_method
    def test_destination(self, message):
        """
        A method-handler a test destination message
        :param message: dict
        :return: dict
        """
        try:
            file_data = self.create_file_to_test_destination
            destination = Destination()
            if message["DestinationInfo"]["DestinationType"] == DESTINATIONS_CONSTS["FTP"] and "Parameters" in message and "SkipTransferringTest" in message["Parameters"] and self.helper.is_text_truemessage["Parameters"]["SkipTransferringTest"]:
                finger_print = destination.test_sftp_destinationmessage
                message_data = {'DestinationInfo':message["DestinationInfo"], 
                 'ResponseData':{"ServerPublicKeyFingerprint": finger_print}, 
                 'IsSuccess':True, 
                 'Message':"", 
                 'Error':None}
            else:
                destination.test_destination(message, file_data["dir"], file_data["file_name"])
                message_data = {'IsSuccess':True,  'Message':"",  'Error':None}
            self.clean_temp_test_filefile_data
            self.mark_message_as_readmessagemessage_data
        except Exception as e:
            try:
                self.clean_temp_test_filefile_data
                raise Exception(self.cm["FAILED_TEST_DEST"].formatstr(e))
            finally:
                e = None
                del e

    @log_method
    def clean_temp_test_file(self, file_data):
        if file_data is not None:
            self.helper.remove_file_or_dir[file_data["dir"] + file_data["file_name"]]

    @log_method
    def create_file_to_test_destination(self):
        file_name = self.helper.get_file_name_for_test
        working_dir = self.local_db.get_working_dir
        self.helper.remove_file_or_dir[working_dir + file_name]
        create_directory(working_dir)
        if not os.path.exists(working_dir + file_name):
            with open(working_dir + file_name, "a+") as f:
                f.write"Test string"
        return {'dir':working_dir, 
         'file_name':file_name}

    @log_method
    def save_job(self, message):
        """
        A method to handle a job settings.
        If message contains destinations and job_destinations, handle them too
        :param message: JSON object
        :return: None
        """
        if "JobId" in message:
            self.add_jobmessage
        if "Destinations" in message:
            self.save_destination(message, should_send_message=False)
        if "JobDestinations" in message:
            self.save_job_destinationmessage["JobDestinations"]message["JobId"]
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def add_job(self, message):
        """
        A method to create new a job
        :param message: dict
        :return: None
        """
        self.local_db.remove_job_triggermessage["JobId"]
        if "JobTriggers" in message:
            if len(message["JobTriggers"]) > 0:
                for trigger in message["JobTriggers"]:
                    self.local_db.add_triggertrigger

        self.local_db.add_jobmessage

    @log_method
    def save_destination(self, message, should_send_message=True):
        """
        A method to save a destination settings
        :param message: dict
        :param should_send_message: bool
        :return: None
        """
        destinations_from_server = []
        if "Destinations" in message:
            for destination in message["Destinations"]:
                destination_id = self.add_destination_and_return_iddestination
                destinations_from_server.appenddestination_id
            else:
                self.delete_absent_destinationsdestinations_from_servermessage["JobId"]

        if should_send_message:
            self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def add_destination_and_return_id(self, destination):
        destination.update{'DestinationName':destination["DestinationName"] if ("DestinationName" in destination) else None, 
         'DestinationType':destination["DestinationType"] if ("DestinationType" in destination) else None, 
         'DestinationSettings':destination["DestinationSettings"] if ("DestinationSettings" in destination) else None, 
         'AccessInfo':self.helper.encrypt_stringdestination["AccessInfo"] if ("AccessInfo" in destination) else None}
        self.local_db.add_destinationdestination
        return destination["DestinationId"]

    @log_method
    def delete_absent_destinations(self, destinations_from_server, job_id):
        """

        :param destinations_from_server:
        :param job_id:
        :return:
        """
        destinations_from_db = self.local_db.get_destinations_idjob_id
        for destination_id in destinations_from_db:
            if destination_id not in destinations_from_server:
                self.local_db.delete_job_destination_by_destination_id_and_job_iddestination_idjob_id
                if len(self.local_db.get_job_destinations_by_destination_iddestination_id) == 0:
                    self.local_db.delete_destination_by_iddestination_id

    @log_method
    def save_job_destination(self, job_destinations, job_id):
        """
        Save job destination
        :param job_destinations: list
        :param job_id: int
        :return: None
        """
        for job_destination in job_destinations:
            self.local_db.add_job_destination(job_id, job_destination["DestinationId"], job_destination["Configuration"] if "Configuration" in job_destination else None, job_destination["Ord"] if "Ord" in job_destination else None)

    @log_method
    def delete_job(self, message=None):
        """
        A method to delete a job
        :param message: dict
        :return: None
        """
        if "JobId" in message:
            if message["JobId"] is not None:
                self.local_db.delete_jobmessage["JobId"]
                self.local_db.remove_destination_and_job_destinationmessage["JobId"]
                self.local_db.remove_job_triggermessage["JobId"]
                self.local_db.remove_objects_backup_result_for_jobmessage["JobId"]
                self.local_db.remove_test_dumps_checksummessage["JobId"]
        if "JobCredentialsId" in message:
            if message["JobCredentialsId"] is not None:
                self.local_db.delete_job_credential_by_idmessage["JobCredentialsId"]
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def run_job(self, message):
        """
        Run job. Get information and then run job
        :param message: JSON object
        :return: None
        """
        self.plain_job.run_job{'JobId':message["JobId"], 
         'JobBackupType':FULL_BACKUP_CONST, 
         'JobMode':BACKUP_JOB_MODE["MANUAL"], 
         'JobInfo':None, 
         'MessageId':message["MessageId"], 
         'SendMessage':self.mark_message_as_read, 
         'Message':message, 
         'IsConsoleMode':False}

    @log_method
    def save_credential_and_get_db_names(self, message):
        """
        Method to save a job credentials
        :param message: Json object
        :return: None
        """
        agent = self.local_db.get_current_agent
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        connection = self.save_job_credential_id_and_return_connectionmessageagent
        db_names_list = self.get_db_namesconnection
        db_data = None
        if connection["ServerType"] == MSSQL_CONST:
            dbms = DBMS(connection)
            db_data = dbms.get_db_data
            if db_data is not None:
                db_data = {(str(connection["ConnectionName"])): db_data}
        self.mark_message_as_readmessage{'SqlServers': None, 'IsSuccess': True, 'Message': '""', 'Error': None, 'SqlServersInfo': db_names_list, 
         'LocalSqlServerInfos': db_data}

    @log_method
    def save_job_credential_id_and_return_connection(self, message, agent):
        connection = self.local_db.get_connection_by_job_cred_idmessage["JobCredentialsId"]
        server_type = self.helper.get_dbms_type_by_nameconnection["ServerType"]connection["ConnectionType"]
        self.local_db.save_job_credential(message["JobCredentialsId"], connection["ConnectionName"], server_type)
        connection["UtilsPath"] = agent["UtilsPath"]
        return connection

    @log_method
    def get_db_names(self, connection):
        dbms = DBMS(connection)
        db_names = [{'Name':db.decode"utf-8" if ("decode" in db) else db, 
         'State':0} for db in dbms.get_databases_names if db]
        return {(connection["ConnectionName"]): db_names}

    @log_method
    def change_account_plan(self, message):
        self.update_down_alert_interval
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def update_user_profile(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def update_agent_configuration(self, message):
        agent = self.local_db.get_current_agent
        if agent is None or agent["AgentKey"] is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        request_result = self.remote_request.get_shortagent["AgentKey"]agent["AgentId"]
        if not request_result["IsSuccess"]:
            raise Exception(self.cm["FAILED_CHECK_IF_SERVER_DELETED"].formatrequest_result["ErrorMessage"])
        elif request_result["Data"]["IsDeleted"]:
            self.local_db.remove_all_database_data
            self.local_db.set_agent_deleted
        else:
            status = self.get_agent_statusagent["AgentKey"]
            if agent["SessionId"] is None:
                agent["SessionId"] = self.helper.get_guid
            self.local_db.update_agent(agent["AgentKey"], status["AgentId"], status["AgentName"], status["AccountName"], status["IsActive"], status["Profile"]["WorkingDir"], agent["SessionId"])
            reset_access_for_working_dir()
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def get_agent_status(self, agent_key):
        request_result = self.remote_request.get_agent_statusagent_key
        if not request_result["IsSuccess"]:
            raise Exception(request_result["ErrorMessage"])
        return request_result["Data"]

    @log_method
    def upload_logs(self, message):
        upload = UploadAppLogs()
        upload.upload_app_logs_to_server
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def activate_logging(self, message):
        if "Configuration" in message:
            message["Configuration"] == "" or self.helper.save_dynamic_settingsmessage["Configuration"]
        else:
            self.helper.update_dynamic_settings_propertyDYNAMIC_SETTING_LOGGING_ACTIVATED"True"
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        UpdateApp().restart_service(mode=(UPDATE_APP_SOURCES["AUTO"]))

    @log_method
    def deactivate_logging(self, message):
        self.helper.update_dynamic_settings_propertyDYNAMIC_SETTING_LOGGING_ACTIVATED"False"
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def upgrade_app(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        if not self.helper.is_app_run_in_docker_container:
            u_app = UpdateApp()
            u_app.update_package((message["Data"]), mode=(UPDATE_APP_SOURCES["MANUALLY"]))

    @log_method
    def check_temp_folder(self, message):
        if not os.path.existsmessage["Path"]:
            raise Exception(self.cm["FAILED_CHECK_TEMP_FOLDER"])
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def restore_backup(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        handle_restore_message(message)

    @log_method
    def download_backup(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        d = Download()
        d.download_resourcemessageFalse

    @log_method
    def download_folder_backup(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        d = Download()
        d.download_resourcemessageTrue

    @log_method
    def cancel_download(self, message):
        agent = self.local_db.get_current_agent
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        for pid in self.local_db.get_processmessage["DownloadId"]PROCESS_TYPES["DOWNLOAD_BACKUP"]:
            self.local_db.delete_processmessage["DownloadId"]PROCESS_TYPES["DOWNLOAD_BACKUP"]
            self.stop_process_and_trace_download(agent["AgentKey"], pid, message)

    @log_method
    def stop_process_and_trace_download(self, agent_key, pid, message):
        if self.helper.stop_process_and_return_is_successpid["Pid"]:
            date_time = str("/Date({0})/".formatself.helper.get_time_in_milliseconds)
            res = self.remote_request.end_download(agent_key, message["DownloadId"], pid["MainRunnerId"], DOWNLOAD_STATUSES["FAILED"], 0, 0, date_time)
            if not res["IsSuccess"]:
                raise Exception(str(res["ErrorMessage"]))

    @log_method
    def cancel_restore_backup(self, message):
        agent = self.local_db.get_current_agent
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        for pid in self.local_db.get_processmessage["RestoreId"]PROCESS_TYPES["RESTORE_BACKUP"]:
            self.local_db.delete_processmessage["RestoreId"]PROCESS_TYPES["RESTORE_BACKUP"]
            self.stop_process_and_trace_restore(pid, agent["AgentKey"], message)

    @log_method
    def stop_process_and_trace_restore(self, pid, agent_key, message):
        if self.helper.stop_process_and_return_is_successpid["Pid"]:
            res = self.remote_request.trace_end_restore(agent_key, message["RestoreId"], pid["MainRunnerId"], RESTORE_STATUSES["CANCELED"], DOWNLOAD_STATUSES["FAILED"], "a restoration was canceled", "")
            if not res["IsSuccess"]:
                raise Exception(str(res["ErrorMessage"]))

    @log_method
    def cancel_job(self, message):
        """
        A method to cancel a job invocation
        :param message:
        :return: None
        """
        agent = self.local_db.get_current_agent
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        json_data = json.loadsmessage["Data"]
        if json_data["BackupId"] is not None:
            try:
                Job().cancel_jobjson_data["BackupId"]
            except Exception as e:
                try:
                    TraceEvent().trace_client_errore"Failed cancelation job."
                finally:
                    e = None
                    del e

        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def cancel_process(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def exec_sql_script(self, message):
        json_data = json.loadsmessage["Data"]
        self.local_db.exec_scriptjson_data["CommandText"]
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def check_server_down_alert(self, message):
        json_data = json.loadsmessage["Data"]
        if json_data["IsActive"]:
            self.update_down_alert_interval
        else:
            self.local_db.update_down_alert_interval0
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def update_down_alert_interval(self):
        agent = self.local_db.get_current_agent
        if agent is None:
            return
        interval = self.get_user_plan_intervalagent["AgentKey"]
        self.local_db.update_down_alert_intervalinterval

    @log_method
    def get_user_plan_interval(self, agent_key):
        agent_info = self.remote_request.get_agent_statusagent_key
        if not agent_info["IsSuccess"]:
            raise Exception(self.cm["FAILED_UPDATE_DOWN_ALERT_INTERVAL"].formatstr(agent_info["ErrorMessage"]))
        return agent_info["Data"]["Profile"]["Plan"]["CheckTimeout"]

    @log_method
    def delete_server(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"The message is ignored",  'Error':None}

    @log_method
    def restart_service(self, message):
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}
        update_app = UpdateApp()
        update_app.restart_service(mode=(UPDATE_APP_SOURCES["AUTO"]))

    @log_method
    def upload_local_db(self, message):
        upload = UploadAppLogs()
        upload.upload_local_db
        self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    @log_method
    def edit_server_name(self, message):
        agent = self.local_db.get_current_agent
        if agent is None:
            return
        else:
            json_data = json.loadsmessage["Data"]
            agent_name = json_data["Name"]
            self.local_db.update_agent_nameagent["AgentKey"]agent_name
            res = self.remote_request.update_agent_name(agent["AgentKey"], agent["AgentId"], agent_name)
            if not res["IsSuccess"]:
                self.local_db.update_agent_nameagent["AgentKey"]agent["AgentName"]
                self.mark_message_as_readmessage{'IsSuccess':False,  'Message':"",  'Error':None}
            else:
                self.mark_message_as_readmessage{'IsSuccess':True,  'Message':"",  'Error':None}

    def get_dbms_connection_settings(self, message):
        try:
            try:
                server_type = 1
                settings = ""
                is_success = True
                error_message = ""
                error = {}
                job_credential_id = message["JobCredentialsId"]
                dbms_connection = self.local_db.get_connection_by_job_cred_idjob_credential_id
                server_name = dbms_connection["ServerType"]
                server_type = self.helper.get_dbms_type_by_nameserver_name"tcp/ip"
                settings = self.connection.get_dbms_connection_settings_as_xmlserver_namedbms_connection
            except Exception as e:
                try:
                    is_success = False
                    error_message = str(e)
                finally:
                    e = None
                    del e

        finally:
            data = {
             'JobCredentialsId': job_credential_id, 
             'ServerType': server_type, 
             'Settings': settings, 
             'IsSuccess': is_success, 
             'Message': error_message, 
             'Error': error}
            self.mark_message_as_readmessagedata

    def save_dbms_connection_settings(self, message):
        try:
            try:
                is_success = True
                error_message = ""
                remote_credential_id = None
                json_data = json.loadsmessage["Data"]
                params = self.connection.get_dbms_connection_settingsjson_data
                if params["job_credential_id"] is None:
                    remote_credential_id = self.connection.add_dbms_connectionparams
                else:
                    dbms_connection = self.local_db.get_connection_by_job_cred_idparams["job_credential_id"]
                    if dbms_connection is None:
                        raise Exception(self.cm["CONNECTION_NOT_FOUND"].formatparams["job_credential_id"])
                    params["connection-id"] = dbms_connection["ConnectionId"]
                    remote_credential_id = self.connection.update_dbms_connectionparams
            except Exception as e:
                try:
                    is_success = False
                    error_message = str(e)
                finally:
                    e = None
                    del e

        finally:
            responce_data = {'JobCredentialsId':remote_credential_id, 
             'ServerType':int(json_data["ServerType"]), 
             'Settings':json_data["Settings"], 
             'IsSuccess':is_success, 
             'Message':error_message, 
             'Error':{}}
            self.mark_message_as_readmessageresponce_data

    def delete_dbms_connection_settings(self, message):
        try:
            try:
                is_success = True
                error_message = ""
                dbms_connection = self.local_db.get_connection_by_job_cred_idmessage["JobCredentialsId"]
                if dbms_connection is None:
                    raise Exception(self.cm["FAILED_GET_CONNECTION"].formatmessage["JobCredentialsId"])
                params = {"connection-id": (dbms_connection["ConnectionId"])}
                self.connection.remove_agent_connection(params, should_print=False)
            except Exception as e:
                try:
                    is_success = False
                    error_message = str(e)
                finally:
                    e = None
                    del e

        finally:
            responce_data = {'IsSuccess':is_success, 
             'Message':error_message, 
             'Error':{}}
            self.mark_message_as_readmessageresponce_data

    def test_dbms_connection(self, message):
        try:
            try:
                is_success = True
                error_message = ""
                agent = self.local_db.get_current_agent
                if agent is None:
                    raise Exception(self.cm["UNREGISTERED_COMP"])
                self.connection.test_dbms_connectionmessage["Data"]agent
            except Exception as e:
                try:
                    is_success = False
                    error_message = str(e)
                finally:
                    e = None
                    del e

        finally:
            responce_data = {'IsSuccess':is_success, 
             'Message':error_message, 
             'Error':{}}
            self.mark_message_as_readmessageresponce_data
