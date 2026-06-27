from sqlbak.logger import log_method
import sqlbak.config.agent_settings
from sqlbak.exchange_message.remote_server_requests import remoute_server_request_instanse
from sqlbak.definitions import DOWNLOAD_STATUSES, RESTORE_STATUSES

class RestoreTracer:
    restore_id = None
    object_id = None

    def __init__(self, message_id, object_id, object_name, job_credentials_id):
        res = remoute_server_request_instanse.trace_begin_restore(sqlbak.config.agent_settings.get_agent_key(), message_id, object_id, object_name, RESTORE_STATUSES["CREATED"], None, job_credentials_id)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        self.restore_id = res["Data"]["RestoreId"]
        self.object_id = object_id

    @log_method
    def download_start(self):
        self.trace_progress(RESTORE_STATUSES["DOWNLOADING"], DOWNLOAD_STATUSES["DOWNLOADING"])

    @log_method
    def download_finish(self):
        self.trace_progress(RESTORE_STATUSES["DOWNLOADED"], DOWNLOAD_STATUSES["DOWNLOADED"])

    @log_method
    def uncompress_start(self):
        self.trace_progress(RESTORE_STATUSES["UNCOMPRESSING"], DOWNLOAD_STATUSES["DOWNLOADED"])

    @log_method
    def uncompress_finish(self):
        self.trace_progress(RESTORE_STATUSES["UNCOMPRESSED"], DOWNLOAD_STATUSES["DOWNLOADED"])

    @log_method
    def restore_start(self):
        self.trace_progress(RESTORE_STATUSES["RESTORING"], DOWNLOAD_STATUSES["DOWNLOADED"])

    @log_method
    def restore_end(self):
        res = remoute_server_request_instanse.trace_end_restore(sqlbak.config.agent_settings.get_agent_key(), self.restore_id, self.object_id, RESTORE_STATUSES["RESTORED"], DOWNLOAD_STATUSES["DOWNLOADED"], "", "")
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def failed(self, message):
        res = remoute_server_request_instanse.trace_end_restore(sqlbak.config.agent_settings.get_agent_key(), self.restore_id, self.object_id, RESTORE_STATUSES["FAILED"], DOWNLOAD_STATUSES["FAILED"], message, "")
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def trace_progress(self, restore_status, download_status):
        res = remoute_server_request_instanse.trace_restore(sqlbak.config.agent_settings.get_agent_key(), self.restore_id, self.object_id, restore_status, download_status, "", "", None)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def trace_end_restore(self, status, message):
        res = remoute_server_request_instanse.trace_end_restore(sqlbak.config.agent_settings.get_agent_key(), self.restore_id, self.object_id, status, DOWNLOAD_STATUSES["DOWNLOADED"], message, "")
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/job_operation/trace.pyc
