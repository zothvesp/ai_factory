import time, json, os
from sqlbak.helpers.util_paths import renew_utils_path
import sqlbak.config.agent_settings
from sqlbak.helpers.permissons import reset_access_for_working_dir
from sqlbak.exchange_message.helper import remove_old_messages
from sqlbak.exchange_message.throttling import check_error_throttling, get_error_count
from sqlbak.plain_job import PlainJob
from sqlbak.daem import Daem
from sqlbak.exchange_message.server_message import ServerMessage
from sqlbak.definitions import PIN_INTERVAL, PROCESS_TYPES, HOUR_IN_MINUTES, MINUTE_IN_SEC, AGENT_UTILS_PATH, ALTERNATIVE_AGENT_UTILS_PATH
from sqlbak.update import UpdateApp
from sqlbak.local_db import LocalDB
from sqlbak.logger import log_error, log_method, log_without_raising, log_data
from sqlbak.dbms.dbms import DBMS
from sqlbak.job import Job
from sqlbak.trace_event import TraceEvent
from sqlbak.helper import Helper
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.job import Job
from sqlbak.process_managment.helper import delete_all_stopped_process, set_subservice_title, cleanup_lost_backup_logs

class App(Daem):

    def __init__(self):
        self.plain_job = PlainJob()
        self.trace_event = TraceEvent()
        self.helper = Helper()
        self.remote_request = RemoteServerRequest()
        self.job = Job()
        self.local_db = LocalDB()
        Daem.__init__(self)

    @log_method
    def start_app(self):
        try:
            self.local_db.create_db_tables_and_update_db_version()
            self.start()
        except Exception as e:
            try:
                self.trace_event.trace_failed_run_app(str(e))
                raise e
            finally:
                e = None
                del e

    @log_without_raising
    def stop_app(self):
        for process in self.local_db.get_processes_by_type(PROCESS_TYPES["BACKUP"]):
            try:
                self.job.cancel_job(process["RunnerId"])
            except Exception:
                pass

    @log_method
    def run(self):
        """
        Method is an enter point into the app
        This method redefine run method from Daem class and start few new process
        :return: None
        """
        reset_access_for_working_dir()
        self.setup_app_settings()
        self.plain_job.remove_cron_taks()
        remove_old_messages(False)
        self.cleanup_process()
        process1 = self.helper.run_additional_process(self.pin_remote_server_service)
        process2 = self.helper.run_additional_process(self.run_backup_log_collector_service)
        process3 = self.helper.run_additional_process(self.scheduled_job_service)
        process4 = self.helper.run_additional_process(self.check_dbms_connections_service)
        process5 = self.helper.run_additional_process(self.check_user_violation_plan_service)
        process6 = self.helper.run_additional_process(self.check_app_updates_service)
        process1.join()
        process2.join()
        process3.join()
        process4.join()
        process5.join()
        process6.join()

    def cleanup_process(self):
        try:
            try:
                delete_all_stopped_process(self.local_db)
            except Exception as e:
                try:
                    self.job.trace_event.failed_run_logs_collector("Failed to manage terminated process: {0}".format(str(e)))
                    raise
                finally:
                    e = None
                    del e

        except Exception as e2:
            try:
                log_error(e2, "Failed died processes cleanup")
            finally:
                e2 = None
                del e2

    @log_method
    def pin_remote_server_service(self):
        set_subservice_title("health-check")
        server_message = ServerMessage()
        while True:
            try:
                sqlbak.config.agent_settings.reload_global_config()
                server_message.pin_remote_server()
                time.sleep(sqlbak.config.agent_settings.pin_interval)
            except Exception as e:
                try:
                    errorMessage = 'The attempt to ping a remote server was unsuccessful ("{0}"). "{1}"'
                    if check_error_throttling(str(e)):
                        self.trace_event.failed_pin_server(errorMessage.format(get_error_count(str(e)), str(e)))
                    time.sleep(PIN_INTERVAL)
                finally:
                    e = None
                    del e

    @log_method
    def run_backup_log_collector_service(self):
        """
        Method to run a backup log collector
        :return: None
        """
        while True:
            try:
                set_subservice_title("backup-log-collector")
                time.sleep(5 * MINUTE_IN_SEC)
                while True:
                    sqlbak.config.agent_settings.reload_global_config()
                    cleanup_lost_backup_logs(self.job)
                    self.helper.delete_log_files_older_then_seven_days()
                    remove_old_messages()
                    time.sleep(30 * MINUTE_IN_SEC)

            except Exception as e:
                try:
                    self.trace_event.failed_run_logs_collector(str(e))
                    time.sleep(1380 * MINUTE_IN_SEC)
                finally:
                    e = None
                    del e

    @log_method
    def scheduled_job_service(self):
        set_subservice_title("schedule-job")
        try:
            while True:
                try:
                    sqlbak.config.agent_settings.reload_global_config()
                    if sqlbak.config.agent_settings.is_active():
                        self.plain_job.check_scheduled_jobs()
                        time.sleep(1)
                    else:
                        time.sleep(10)
                except Exception as e:
                    try:
                        self.trace_event.failed_to_handle_scheduled_job('Failed to verify scheduled jobs: "{0}"'.format(str(e)))
                        time.sleep(55)
                    finally:
                        e = None
                        del e

        except:
            time.sleep(299)
            self.scheduled_job_service()

    @log_method
    def check_app_updates_service(self):
        set_subservice_title("app-update")
        if not self.helper.is_app_run_in_docker_container():
            try:
                time.sleep(3 * MINUTE_IN_SEC)
                while True:
                    sqlbak.config.agent_settings.reload_global_config()
                    u_app = UpdateApp()
                    u_app.update_package()
                    time.sleep(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC)

            except Exception as e:
                try:
                    self.trace_event.failed_check_app_updates('Failed to update the app by an auto mode. "{0}"'.format(str(e)))
                    time.sleep(23 * HOUR_IN_MINUTES * MINUTE_IN_SEC)
                    self.check_app_updates()
                finally:
                    e = None
                    del e

    @log_method
    def check_dbms_connections_service(self):
        while True:
            try:
                set_subservice_title("dbms-health-check")
                while True:
                    while True:
                        sqlbak.config.agent_settings.reload_global_config()
                        interval = self.local_db.get_down_alert_interval()
                        if interval == 0:
                            time.sleep(10)

                    dbms = DBMS()
                    dbms.check_dbms_connections()
                    time.sleep(interval)

            except Exception as e:
                try:
                    self.trace_event.failed_check_dbms_connections(str(e))
                    time.sleep(1380 * MINUTE_IN_SEC)
                finally:
                    e = None
                    del e

    @log_method
    def check_user_violation_plan_service(self):
        try:
            set_subservice_title("user-plan")
            while True:
                sqlbak.config.agent_settings.reload_global_config()
                server_message = ServerMessage()
                server_message.update_down_alert_interval()
                time.sleep(4 * HOUR_IN_MINUTES * MINUTE_IN_SEC)

        except Exception as e:
            try:
                self.trace_event.failed_check_user_violation_plan('Failed to check a user violation plan. "{0}"'.format(str(e)))
                time.sleep(4 * HOUR_IN_MINUTES * MINUTE_IN_SEC)
                self.check_user_violation_plan()
            finally:
                e = None
                del e

    @log_method
    def setup_app_settings(self):
        try:
            agent = self.local_db.get_current_agent()
            if agent is not None:
                self.local_db.update_agent_version()
                agent = self.local_db.get_current_agent()
                agent["SessionId"] = None
                agent["SessionId"] = self.helper.update_agent_session(agent, self.local_db)
                log_data("Session id: {0}".format(agent["SessionId"]))
                agent_utils = json.loads(agent["UtilsPath"])
                renew_utils_path(agent_utils)
                self.local_db.update_agent_utils_path(agent["AgentKey"], agent_utils)
                res = self.remote_request.update_agent(agent, json.loads(agent["UtilsPath"]))
                if "IsConnectionError" in res and res["IsConnectionError"]:
                    log_data(res["ErrorMessage"])
                elif not res["IsSuccess"]:
                    raise Exception(str(res["ErrorMessage"]))
        except Exception as e:
            try:
                self.trace_event.trace_client_error(e, "Error send application settings to server:")
            finally:
                e = None
                del e

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/app.pyc
