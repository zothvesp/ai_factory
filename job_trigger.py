
import json, time
from sqlbak.logger import log_data, log_method, log_only_exception
from sqlbak.job_log import JobLog
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.helper import Helper
from sqlbak.job import Job
from sqlbak.definitions import MESSAGE_TYPES_CONSTS, DESTINATIONS_NAMES, CONFIG, RESTORE_STATUSES, HOUR_IN_MINUTES, MINUTE_IN_SEC
from sqlbak.app_output import APP_OUTPUT

class JobTrigger(Job):

    def __init__(self, params):
        Job.__init__(self)
        self.params = params
        self.job_log = JobLog()
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.helper = Helper()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def run(self):
        if len(self.params["JobTriggers"]) > 0:
            self.params = self.job_log.start_restore_by_trigger(self.params)
        for trigger in self.params["JobTriggers"]:
            if not "BackupTypeForTrigger" not in self.params:
                if self.params["BackupTypeForTrigger"] not in trigger["BackupTypes"]:
                    pass
                else:
                    server_name = self.get_server_name_by_agent_id(self.params["AgentKey"], trigger["AgentId"], self.params["AgentId"], self.params["ClientName"])
            for db in trigger["Databases"]:
                try:
                    self.check_if_backup_is_success(trigger["DestinationId"], db["SourceDb"])
                    out_id = self.get_object_id(trigger["DestinationId"], db["SourceDb"], self.params["BackupId"])
                    self.params = self.job_log.trace_trigger_restore(self.params, db["DestinationDb"], db["SourceDb"], server_name)
                    message = self.get_message_for_restore(trigger, db, out_id)
                    message_id = self.send_message_to_another_server(message, trigger["AgentId"])
                    res = self.helper.run_method_with_number_attempts_and_timeout(self, "check_restore_on_another_server", is_instance=True, attempts=3, params=(message_id,), time_out=(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC))
                    self.handle_restore_result(res)
                except Exception as e:
                    try:
                        self.catch_job_error(self.cm["FAILED_RESTORE_TRIGGER"].format(db["SourceDb"], str(e)))
                    finally:
                        e = None
                        del e

        if len(self.params["JobTriggers"]) > 0:
            self.send_unsend_backup_logs(self.params["BackupId"], self.params["JobMode"])

    @log_method
    def get_object_id(self, destination_id, db_name, backup_id):
        object_id = self.local_db.get_backup_object_id(destination_id, db_name, backup_id)
        if object_id is None:
            error = self.cm["FAILED_RUN_TRIGGER"]
            self.params = self.job_log.failed_to_restore_backup(self.params, db_name, error)
            raise Exception(error)
        return object_id

    @log_method
    def get_message_for_restore(self, trigger, db, object_id):
        destination = self.local_db.get_destination_by_id(trigger["DestinationId"])
        if destination is None:
            self.job_log.trigger_restore_destination_failed(self.params, db["DestinationDb"], db["SourceDb"], self.params["ClientName"], DESTINATIONS_NAMES[destination["DestinationType"]], destination["DestinationSettings"])
        return {'BackupObjectId':object_id, 
         'ObjectName':db["DestinationDb"], 
         'JobCredentialsId':trigger["JobCredentialsId"], 
         'ArchivesPassword':self.params["CompressionPassword"], 
         'DisconnectApplications':True, 
         'DestinationInfo':{'DestinationType':destination["DestinationType"], 
          'DestinationVersion':2, 
          'DestinationSettings':destination["DestinationSettings"], 
          'AccessInfo':(self.helper.decrypt_string)(destination["AccessInfo"]), 
          'DestinationId':trigger["DestinationId"], 
          'DestinationName':destination["DestinationName"]}, 
         'LocalSqlServerSettings':db["LocalSqlServerSettings"], 
         'Scripts':trigger["RestoreScripts"]}

    @log_method
    def send_message_to_another_server(self, message, agent_id):
        data = {'MessageId':None, 
         'MessageType':str(MESSAGE_TYPES_CONSTS["RESTORE_BACKUP"]), 
         'MessageData':(json.dumps)(message), 
         'IsToServer':False, 
         'IsResponseExpected':True}
        res = self.remote_request.send_message(str(self.params["AgentKey"]), data, agent_id)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        return res["Data"]["MessageId"]

    @log_method
    def check_restore_on_another_server(self, message_key):
        agent = self.local_db.get_current_agent()
        check_result = None
        message_id = None
        while True:
            message_id = self.get_message_by_id(agent, message_key)
            if message_id is not None:
                break

        while True:
            responce = self.get_info_by_message(agent, message_id)
            if responce is not None:
                check_result = responce
                break

        return check_result

    @log_only_exception
    def get_message_by_id(self, agent, message_id):
        time.sleep(2)
        res = self.remote_request.get_message(agent["AgentKey"], message_id)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        if res["Data"]["IsToServer"]:
            return res["Data"]["MessageId"]
        return

    @log_only_exception
    def get_info_by_message(self, agent, message_id):
        time.sleep(2)
        res = self.remote_request.get_info_by_message(agent["AgentKey"], message_id)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        restore_status = self.get_restore_status(res["Data"])
        return restore_status

    @log_only_exception
    def get_restore_status(self, data):
        correct_statuses = [RESTORE_STATUSES["RESTORED"], RESTORE_STATUSES["FAILED"], RESTORE_STATUSES["CANCELED"]]
        if not data is None:
            if "Status" not in data or data["Status"] is None or int(data["Status"]) not in correct_statuses:
                return
            return {'status':int(data["Status"]), 
             'message':data["Message"]}

    @log_method
    def handle_restore_resultParse error at or near `LOAD_FAST' instruction at offset 0

    @log_method
    def get_server_name_by_agent_id(self, agent_key, trigger_agent_id, agent_id, client_name):
        if int(trigger_agent_id) != int(agent_id):
            res = self.remote_request.get_short(agent_key, trigger_agent_id)
            if not res["IsSuccess"]:
                raise Exception(str(res["ErrorMessage"]))
            client_name = res["Data"]["AgentName"]
        return client_name

    @log_method
    def check_if_backup_is_success(self, destination_id, source_db):
        is_backup_success = False
        for o in self.params["ObjectBackupResults"]:
            for d in o["destinations"]:
                if int(d["destination_id"]) == int(destination_id):
                    if bool(d["is_success"]):
                        if o["object_name"] == source_db:
                            is_backup_success = True

        if not is_backup_success:
            raise Exception(self.cm["BACKUP_FAILED_NO_RESTORE"])
