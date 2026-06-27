import json, time
from datetime import datetime, timedelta
from sqlbak.logger import log_method, log_only_exception
from sqlbak.job_log import JobLog
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.helper import Helper
from sqlbak.definitions import CONFIG, TIMEOUT, DESTINATIONS_CONSTS, FULL_BACKUP_CONST, FOLDER_BACKUP_CONST, HOUR_IN_MINUTES, MINUTE_IN_SEC, SEVERITY_PARAMS
from sqlbak.job import Job
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist

class Cleanup(Job):

    def __init__(self, params):
        Job.__init__(self)
        self.params = params
        self.job_log = JobLog()
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.helper = Helper()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def clean_old_backups(self):
        try:
            self.params = self.job_log.cleanup_job_log(self.params)
            backups_to_cleanup = self.get_backup_objects_for_cleanup()
            self.cleanup(backups_to_cleanup)
        except Exception as e:
            try:
                self.catch_job_error(self.cm["FAILED_CLEAN_OVERDUE_BACKUP"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_backup_objects_for_cleanup(self):
        backups_to_cleanup = []
        for backup in self.params["ObjectBackupResults"]:
            if backup["is_success"]:
                backups_to_cleanup.append(backup)
            return backups_to_cleanup

    @log_method
    def cleanup(self, backups_to_cleanup):
        backup_object_ids = []
        for backup in backups_to_cleanup:
            for destination in backup["destinations"]:
                should_cleanup = self.should_cleanup_be_done(destination["destination_id"], backup["backup_type"])
                try:
                    for overdue_backup in self.get_overdue_backups_for_cleanup(destination, backup):
                        self.delete_overdue_backup(destination, overdue_backup, should_cleanup, backup["backup_type"])

                    if overdue_backup["BackupObjectId"] not in backup_object_ids:
                        backup_object_ids.append(overdue_backup["BackupObjectId"])
                except Exception as e:
                    try:
                        self.catch_job_error(str(e))
                    finally:
                        e = None
                        del e

            if len(backup_object_ids) > 0:
                try:
                    self.remove_files_by_object_id_on_server(backup_object_ids)
                except Exception as e:
                    try:
                        self.catch_job_error(str(e))
                    finally:
                        e = None
                        del e

                else:
                    backup_object_ids = []

    @log_only_exception
    def should_cleanup_be_done(self, destination_id, backup_type):
        """

        :param destination_id:
        :param backup_type:
        :return:
        """
        last_backup_cleanup = self.local_db.get_last_backup_cleanup_time(self.params["JobId"], destination_id)
        if last_backup_cleanup is None or backup_type in (FULL_BACKUP_CONST, FOLDER_BACKUP_CONST):
            should_cleanup = True
        else:
            cleanup_time = self.helper.get_date_time(last_backup_cleanup["LastCleanupAt"]) + timedelta(hours=1)
            should_cleanup = cleanup_time < datetime.now()
        return should_cleanup

    @log_method
    def delete_overdue_backup(self, destination, backup, should_cleanup, backup_type):
        """

        :param destination:
        :param backup:
        :param should_cleanup:
        :return:
        """
        try:
            destination["instance"] = self.get_destination_instance(destination)
            for object_file in backup["ObjectFileInfos"]:
                if should_cleanup:
                    self.delete_backup_file_at_destination_if_exists(destination["instance"], object_file["FileName"], backup_type, object_file["OutId"])
            else:
                if should_cleanup:
                    self.local_db.add_job_destination_data(self.params["JobId"], destination["destination_id"])
                destination["instance"].close_connection()

        except Exception as e:
            try:
                self.catch_job_error(self.cm["FAILED_DELETE_OVERDUE_BACKUP"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_destination_instance(self, destination):
        if destination["settings"]["DestinationType"] in (DESTINATIONS_CONSTS["GOOGLE"], DESTINATIONS_CONSTS["ONEDRIVE"], DESTINATIONS_CONSTS["ONEDRIVE_BUSINESS"]):
            d = self.job_settings.get_destination_settings_by_job_id(self.params["JobId"], destination["destination_id"])
            destination["instance"] = d["instance"]
        return destination["instance"]

    @log_method
    def delete_backup_file_at_destination_if_exists(self, instance, backup_name, backup_type, outId):
        try:
            self.params = self.job_log.delete_file(self.params, backup_name)
            instance.connect()
            try:
                self.helper.run_method_with_number_attempts_and_timeout(instance, "delete_file", params=(backup_name, outId), is_instance=True, attempts=4, time_out=(5 * HOUR_IN_MINUTES * MINUTE_IN_SEC))
            except DestinationFileDoesNotExist:
                self.params["Severity"] = SEVERITY_PARAMS["Warning"]
                if backup_type == FOLDER_BACKUP_CONST:
                    self.job_log.folder_is_not_found_at_destination(self.params, backup_name)
                else:
                    self.job_log.file_is_not_found_at_destination(self.params, backup_name)
                self.params["Severity"] = SEVERITY_PARAMS["Info"]

        except Exception as e:
            try:
                self.catch_job_error(self.cm["FAILED_DELETE_OVERDUE_BACKUP"].format(str(e)))
            finally:
                e = None
                del e

    @log_only_exception
    def get_overdue_backups_for_cleanup(self, destination, backup):
        """

        :param destination:
        :param backup:
        :return:
        """
        datetime_params = self.get_datetime_params(destination, backup)
        return self.get_backups_data_from_server(datetime_params)

    @log_method
    def get_datetime_params(self, destination, backup):
        keep_days = int(destination["settings"]["KeepDays"])
        keep_months = int(destination["settings"]["KeepMonths"])
        inc_keep_days = int(destination["settings"]["IncKeepDays"])
        inc_keep_months = int(destination["settings"]["IncKeepMonths"])
        return {'JobId':int(self.params["JobId"]), 
         'DestinationId':int(destination["destination_id"]), 
         'BackupObjectType':int(backup["object_type"]), 
         'ObjectName':str(backup["object_name"]), 
         'KeepFullBackups':("P{}D".format)(keep_months * 30 + keep_days), 
         'KeepIncBackups':("P{}D".format)(inc_keep_months * 30 + inc_keep_days)}

    @log_method
    def get_backups_data_from_server(self, datetime_params):
        res = self.remote_request.get_backups_for_cleanup(datetime_params)
        if not res["IsSuccess"]:
            raise Exception(str(res["ErrorMessage"]))
        return res["Data"]

    @log_method
    def remove_files_by_object_id_on_server(self, object_ids):
        if len(object_ids) > 0:
            res = self.remote_request.remove_backup_files_list(object_ids)
            if not res["IsSuccess"]:
                raise Exception(str(res["ErrorMessage"]))

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/cleanup.pyc
