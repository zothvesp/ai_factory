from logging import error
import os, re, json
from sqlbak.definitions import EVENTS_ID, EVENT_TYPES, CONFIG
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
from sqlbak.logger import log_data, log_method, log_without_raising, logger_handler

class TraceEvent:

    def __init__(self):
        self.remote_request = RemoteServerRequest()
        self.local_db = LocalDB()
        self.helper = Helper()

    @log_without_raising
    def get_agent_and_event_data_to_trace_application_event(self, event_type, event_data, event_source):
        agent = self.get_agent_data()
        data = {'EventId':str(self.helper.get_guid()), 
         'InstallationId':str(self.get_installation_id()), 
         'SessionId':str(agent["SessionId"]), 
         'EventSource':str(event_source), 
         'EventType':str(event_type), 
         'EventData':str(event_data), 
         'ApplicationTypeId':2, 
         'TimeStamp':str("/Date({0})/".format(self.helper.get_time_in_milliseconds())), 
         'MajorVersion':str(agent["MajorVersion"]), 
         'MinorVersion':str(agent["MinorVersion"]), 
         'PatchVersion':str(agent["PatchVersion"]), 
         'ApplicationKey':str(agent["AgentKey"]) if (agent["AgentKey"] is not None) else None}
        return data

    @log_method
    def get_agent_data(self):
        agent = self.get_default_agent_data()
        agent["SessionId"] = self.helper.update_agent_session(agent, self.local_db)
        return agent

    @log_method
    def get_default_agent_data(self):
        agent = self.local_db.get_current_agent()
        if agent is None:
            agent = {'SessionId':(self.helper.get_guid)(),  'MajorVersion':1, 
             'MinorVersion':1, 
             'PatchVersion':1, 
             'AgentKey':None}
        return agent

    @log_method
    def get_installation_id(self):
        path_to_installation_id = CONFIG["PATH_TO_INSTALL_ID"]
        installation_id = self.get_existing_installation_id(path_to_installation_id)
        if installation_id is not None:
            return installation_id
        return self.create_new_installation_id(path_to_installation_id)

    @log_method
    def get_existing_installation_id(self, path_to_file):
        installation_id = None
        if os.path.exists(path_to_file):
            with open(path_to_file, "r") as f:
                file_content = f.read()
                if self.is_string_correct_guid(str(file_content)):
                    installation_id = str(file_content)
        return installation_id

    @log_method
    def create_new_installation_id(self, path_to_file):
        installation_id = self.helper.get_guid()
        with open(path_to_file, "w") as f:
            f.write(str(installation_id))
        return str(installation_id)

    def is_string_correct_guidParse error at or near `SETUP_FINALLY' instruction at offset 0

    def get_agent_and_event_data_to_trace_client_event(self, event_id, event_type, event_data, stack_trace='', details='', visbility=False):
        return {'CreatedAt':str("/Date({0})/".format(self.helper.get_time_in_milliseconds())), 
         'EntryType':int(event_type), 
         'EventId':int(event_id), 
         'Message':str(event_data), 
         'StackTrace':str(stack_trace), 
         'Visible':visbility, 
         'Details':str(details), 
         'Parameters':[]}

    @log_method
    def trace_failed_run_app(self, error):
        event_type = "Run"
        event_data = {'Status':"Failed", 
         'ErrorMessage':error}
        event_source = "App"
        data = self.get_agent_and_event_data_to_trace_application_event(event_type, json.dumps(event_data), event_source)
        if data:
            self.remote_request.trace_application_event(data)

    @log_without_raising
    def trace_register_app(self):
        event_type = "Registration"
        event_data = {'Status':"Success", 
         'ErrorMessage':None}
        event_source = "App"
        data = self.get_agent_and_event_data_to_trace_application_event(event_type, json.dumps(event_data), event_source)
        if data:
            self.remote_request.trace_application_event(data)

    @log_method
    def trace_restart_service(self, mode):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = "restart service. mode: {0}".format(mode)
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["FORCE_UPDATE"], EVENT_TYPES["INFO"], event_data)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_pin_server(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["ERROR"], EVENT_TYPES["ERROR"], error_message)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_run_logs_collector(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = "Failed to delete application logs: {0}".format(error_message)
            data = self.get_agent_and_event_data_to_trace_client_event((EVENTS_ID["ERROR"]), (EVENT_TYPES["ERROR"]), event_data, visbility=True)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_to_handle_scheduled_job(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = "Failed to handle the scheduled job: {0}".format(error_message)
            data = self.get_agent_and_event_data_to_trace_client_event((EVENTS_ID["ERROR"]), (EVENT_TYPES["ERROR"]), event_data, visbility=True)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_check_app_updates(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = "failed check updates. {0}".format(error_message)
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["ERROR"], EVENT_TYPES["ERROR"], event_data)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_check_dbms_connections(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = 'Failed to verify database availability: "{0}"'.format(error_message)
            data = self.get_agent_and_event_data_to_trace_client_event((EVENTS_ID["ERROR"]), (EVENT_TYPES["ERROR"]), event_data, visbility=True)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_check_user_violation_plan(self, error_message):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = "failed check user violations. {0}".format(error_message)
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["ERROR"], EVENT_TYPES["ERROR"], event_data)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def failed_update_package(self, msg):
        agent = self.local_db.get_current_agent()
        if agent is not None:
            event_data = msg
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["ERROR"], EVENT_TYPES["ERROR"], event_data)
            self.remote_request.trace_client_event(agent["AgentKey"], data)

    @log_without_raising
    def trace_console_command(self, data):
        event_type = data["Type"]
        event_data = json.dumps(data["Data"])
        event_source = "App>Console"
        res = self.get_agent_and_event_data_to_trace_application_event(event_type, event_data, event_source)
        if res:
            self.remote_request.trace_application_event(res)

    @log_method
    def trace_client_error(self, exception, error_message=None):
        try:
            msg = str(exception) if error_message == None else "{0}. {1}".format(error_message, str(exception))
            agent = self.local_db.get_current_agent()
            msg = msg.replace(agent["AgentKey"], '"' + agent["AgentKey"] + '"')
            data = self.get_agent_and_event_data_to_trace_client_event(EVENTS_ID["ERROR"], EVENT_TYPES["ERROR"], msg)
            self.remote_request.trace_client_event(agent["AgentKey"], data)
        except Exception as e:
            try:
                logger_handler.log_error(self.trace_client_error, e)
            finally:
                e = None
                del e

    @log_method
    def trace_client_message(self, message, visibility=True):
        try:
            agent = self.local_db.get_current_agent()
            data = self.get_agent_and_event_data_to_trace_client_event((EVENTS_ID["ERROR"]), (EVENT_TYPES["INFO"]), message, visbility=visibility)
            self.remote_request.trace_client_event(agent["AgentKey"], data)
        except Exception as e:
            try:
                logger_handler.log_error(self.trace_client_error, e)
            finally:
                e = None
                del e


__trace_event_instanse = None

def get_instanse():
    global __trace_event_instanse
    if __trace_event_instanse is None:
        __trace_event_instanse = TraceEvent()
    return __trace_event_instanse


def trace_app_error(exception=None, error_message=None):
    if exception is None:
        exception = Exception("ClientError:")
    get_instanse().trace_client_error(exception, error_message)


def trace_app_message(message, visibility=True):
    get_instanse().trace_client_message(message, visibility)


trace_event_instanse = get_instanse()
