from datetime import datetime
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_method
from sqlbak.definitions import CONFIG, COMPRESSION_LEVEL_DEFAULT, COMPRESSION_LEVELS, COMPRESSION_ENGINE_ZIP, ZIP_EXT
from sqlbak.app_output import APP_OUTPUT
from sqlbak.helpers.temporary_directory import create_directory, get_correct_path

class UploadAppLogs:

    def __init__(self):
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.helper = Helper()
        self.native_command = NativeCommand()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def upload_app_logs_to_server(self):
        agent = self.local_db.get_current_agent()
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        path_to_app = get_correct_path(CONFIG["PATH_TO_APP"])
        path_to_logs = path_to_app + CONFIG["PATH_TO_LOGS"]
        path_to_compressed_logs = path_to_app + CONFIG["PATH_TO_COMPRESSED_LOGS"]
        self.compress_app_logs(path_to_compressed_logs, path_to_logs)
        self.send_compressed_app_log_files_to_server(path_to_compressed_logs, agent["AgentKey"])

    @log_method
    def compress_app_logs(self, path_to_compressed_logs, path_to_logs):
        self.helper.remove_file_or_dir([path_to_compressed_logs])
        create_directory(path_to_compressed_logs)
        for log_file in self.helper.get_files_in_directory(path_to_logs):
            self.native_command.compress_backup_by_zip(COMPRESSION_LEVELS[COMPRESSION_ENGINE_ZIP][COMPRESSION_LEVEL_DEFAULT], "", False, path_to_compressed_logs + log_file + ZIP_EXT, path_to_logs + log_file, log_file, path_to_logs)

    @log_method
    def send_compressed_app_log_files_to_server(self, path_to_compressed_logs, agent_key):
        session_id = self.get_session_id()
        for log_file in self.helper.get_files_in_directory(path_to_compressed_logs):
            self.upload_file_by_chunks(path_to_compressed_logs + log_file, agent_key, session_id, log_file)
        else:
            self.remote_request.send_log_to_developers(agent_key, session_id)

    @log_method
    def get_session_id(self):
        now = datetime.now()
        session_id = str(now.strftime("%d-%m-%Y_%H:%M:%S")) + "_" + self.helper.get_uuid()
        return session_id

    @log_method
    def upload_file_by_chunks(self, path_to_compressed_logs, agent_key, session_id, file_name):
        file_in_bytes = open(path_to_compressed_logs, "rb")
        for chunk in self.helper.read_file_by_chunks(file_in_bytes):
            res = self.remote_request.upload_file_chunk(agent_key, session_id, file_name, chunk)
            if not res["IsSuccess"]:
                raise Exception(str(res["ErrorMessage"]))

    @log_method
    def upload_local_db(self):
        agent = self.local_db.get_current_agent()
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        path_to_app = get_correct_path(CONFIG["PATH_TO_APP"])
        path_to_local_db = path_to_app + CONFIG["DB_NAME"]
        path_to_copy = path_to_local_db + ".copy"
        file_name = "sqlbak.db.zip"
        try:
            self.compress_local_db(path_to_local_db, path_to_copy, CONFIG["DB_NAME"])
            self.send_compressed_local_db_to_server(path_to_copy + ZIP_EXT, file_name, agent["AgentKey"])
            self.helper.remove_file_or_dir([path_to_copy, path_to_copy + ZIP_EXT])
        except Exception as e:
            try:
                self.helper.remove_file_or_dir([path_to_copy, path_to_copy + ZIP_EXT])
                raise Exception(e)
            finally:
                e = None
                del e

    @log_method
    def compress_local_db(self, path_to_local_db, path_to_copy, file_name):
        self.native_command.copy_resource(path_to_local_db, path_to_copy)
        self.native_command.compress_backup_by_zip(COMPRESSION_LEVELS[COMPRESSION_ENGINE_ZIP][COMPRESSION_LEVEL_DEFAULT], "", False, path_to_copy + ZIP_EXT, path_to_copy, file_name, path_to_copy)

    @log_method
    def send_compressed_local_db_to_server(self, path_to_file, file_name, agent_key):
        session_id = self.get_session_id()
        self.upload_file_by_chunks(path_to_file, agent_key, session_id, file_name)
        self.remote_request.send_log_to_developers(agent_key, session_id)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/upload.pyc
