from datetime import datetime
import os
from sqlbak.logger import log_method
from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.destinations.destination import Destination
from sqlbak.dbms.dbms import DBMS
from sqlbak.definitions import CONFIG, PROCESS_TYPES, DOWNLOAD_STATUSES, TIMEOUT, HOUR_IN_MINUTES, MINUTE_IN_SEC
from sqlbak.app_output import APP_OUTPUT
from sqlbak.helpers.temporary_directory import create_directory

class Download:

    def __init__(self):
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.helper = Helper()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def download_resource(self, message, is_folder):
        """

        :param message: dict
        :param is_folder: bool
        :return:
        """
        agent = self.local_db.get_current_agent()
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        working_dir = self.local_db.get_working_dir()
        tmp_dir = self.create_temp_directory(working_dir)
        backup_object = self.get_backup_object(message["BackupObjectId"])
        download_id = self.get_backup_download_id(message, working_dir, backup_object, is_folder)
        try:
            for obj in backup_object["ObjectFileInfos"]:
                backup_settings = self.get_backup_settings(backup_object, obj["FileName"])
                file_name = str(backup_settings["FileName"])
                if "OutId" in obj:
                    outId = str(obj["OutId"])
                else:
                    outId = None
                destination_instance = self.get_destination_instance(backup_settings["DestinationInfo"])
                self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "connect", is_instance=True, attempts=4, time_out=(2 * TIMEOUT))
                self.check_if_backup_exist_at_destination(destination_instance, file_name, outId)
                file_size = self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "get_uploaded_file_size", is_instance=True, params=(file_name, outId), attempts=4, time_out=(5 * MINUTE_IN_SEC))
                self.trace_begin_download(agent["AgentKey"], download_id, obj, file_size)
                self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "download_file", is_instance=True, params=(file_name, working_dir, outId), attempts=4, time_out=(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC))
                self.check_if_file_exist_locally(working_dir + file_name)
                self.trace_end_file_download(agent["AgentKey"], download_id, obj, file_size)
            else:
                self.clean_temp_data(is_folder, download_id, tmp_dir)
                self.trace_end_download(agent["AgentKey"], download_id, message, DOWNLOAD_STATUSES["DOWNLOADED"])

        except Exception as e:
            try:
                self.clean_temp_data(is_folder, download_id, tmp_dir)
                if download_id is not None:
                    self.trace_end_download(agent["AgentKey"], download_id, message, DOWNLOAD_STATUSES["FAILED"], backup_object["ArchiveSize"])
            finally:
                e = None
                del e

    @log_method
    def create_temp_directory(self, parent_path_to):
        now = datetime.now()
        working_dir = parent_path_to + str(now.strftime("%Y%m%d%H%M")) + "/"
        self.helper.remove_file_or_dir([working_dir])
        create_directory(working_dir)
        return working_dir

    @log_method
    def get_backup_object(self, object_id):
        object_info = self.remote_request.get_backup_object_info(object_id)
        if not object_info["IsSuccess"]:
            raise Exception(str(object_info["ErrorMessage"]))
        return object_info["Data"]

    @log_method
    def get_backup_download_id(self, message, working_dir, backup_object, is_folder):
        date_time = str("/Date({0})/".format(self.helper.get_time_in_milliseconds()))
        res = self.remote_request.begin_download(message["MessageId"], message["BackupObjectId"], working_dir, backup_object["ArchiveSize"], date_time)
        if not res["IsSuccess"]:
            raise Exception(res["ErrorMessage"])
        download_id = res["Data"]["DownloadId"]
        self.local_db.add_process(os.getpid(), download_id, message["BackupObjectId"], PROCESS_TYPES["DOWNLOAD_FOLDER" if is_folder else "DOWNLOAD_BACKUP"])
        return download_id

    @log_method
    def get_backup_settings(self, backup_object, file_name):
        destination = self.local_db.get_destination_by_id(backup_object["DestinationId"])
        return {'FileName':file_name, 
         'ArchiveSize':backup_object["ArchiveSize"], 
         'Folder':backup_object["Folder"], 
         'DestinationInfo':{'DestinationId':destination["DestinationId"], 
          'DestinationType':destination["DestinationType"], 
          'AccessInfo':destination["AccessInfo"], 
          'DestinationSettings':destination["DestinationSettings"], 
          'DestinationName':destination["DestinationName"], 
          'DestinationPath':backup_object["Folder"] if (backup_object["Folder"] is not None) else ""}}

    @log_method
    def get_destination_instance(self, destination_info):
        destination = Destination()
        return destination.get_destination_instance(destination_info)

    @log_method
    def check_if_backup_exist_at_destination(self, destination_instance, file_name, outid):
        is_file_exist = self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "is_file_exist", params=(file_name, outid), is_instance=True, attempts=4, time_out=(5 * MINUTE_IN_SEC))
        if not is_file_exist:
            raise Exception(self.cm["FILE_NOT_EXISTS_DEST"].format(file_name))

    @log_method
    def trace_begin_download(self, agent_key, download_id, obj, file_size):
        date_time = str("/Date({0})/".format(self.helper.get_time_in_milliseconds()))
        res = self.remote_request.begin_file_download(agent_key, download_id, obj["BackupObjectFileId"], int(file_size), date_time)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def check_if_file_exist_locally(self, path_to_resource):
        if not os.path.exists(path_to_resource):
            raise Exception(self.cm["FILE_NOT_EXISTS"].format(str(path_to_resource)))

    @log_method
    def trace_end_file_download(self, agent_key, download_id, obj, file_size):
        date_time = str("/Date({0})/".format(self.helper.get_time_in_milliseconds()))
        res = self.remote_request.end_file_download(agent_key, download_id, obj["BackupObjectFileId"], 100, int(file_size), DOWNLOAD_STATUSES["DOWNLOADED"], "", date_time)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def trace_end_download(self, agent_key, download_id, message, status, file_size=None):
        date_time = str("/Date({0})/".format(self.helper.get_time_in_milliseconds()))
        res = self.remote_request.end_download(agent_key, download_id, message["BackupObjectId"], status, 100, file_size, date_time)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))

    @log_method
    def clean_temp_data(self, is_folder, download_id, working_dir):
        if working_dir:
            self.helper.remove_file_or_dir([working_dir])
        if download_id is not None:
            self.local_db.delete_process(download_id, PROCESS_TYPES["DOWNLOAD_FOLDER" if is_folder else "DOWNLOAD_BACKUP"])

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/download.pyc
