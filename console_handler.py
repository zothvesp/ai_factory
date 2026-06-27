import json, socket
from datetime import date
from sqlbak.config.agent_settings import reload_global_config
from sqlbak.console_parser import ConsoleParser
from sqlbak.definitions import CONSOLE_COLORS, AVAILABLE_SERVER_TYPES, CONFIG, AGENT_UTILS_PATH, BACKUP_JOB_MODE, FULL_BACKUP_CONST, MYSQLDUMP_CONST, MYSQL_CONST
from sqlbak.definitions import REQUEST_PATH_CONSTS, DYNAMIC_SETTING_LOGGING_ACTIVATED, UPDATE_APP_SOURCES, DOCKER_EXEC, SUDO_SQLBAK, PORTS_SCOPE
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.dbms.dbms import DBMS
from sqlbak.plain_job import PlainJob
from sqlbak.logger import log_method, log_only_exception
from sqlbak.app import App
from sqlbak.update import UpdateApp
from sqlbak.upload import UploadAppLogs
from sqlbak.native_command import NativeCommand
from sqlbak.trace_event import TraceEvent, trace_app_message
from sqlbak.app_output import APP_OUTPUT
from sqlbak.connection import Connection
from sqlbak.exceptions import ConsoleCommandError
from sqlbak.process_managment.helper import cleanup_lost_backup_logs
from sqlbak.job import Job
from sqlbak.helpers.app_registration import register_app, unregister_app, register_new_agent_on_the_sqlbak_server
from sqlbak.helpers.database_interactive_connector import main_menu, add_database_menu

class ConsoleHandler:

    def __init__(self):
        self.helper = Helper()
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.plain_job = PlainJob()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.console_parser = ConsoleParser()
        self.trace_event = TraceEvent()
        self.connection = Connection()

    @log_method
    def parse_console_command_with_params(self, console_params):
        """
        A method to receive a passed command and params
        :param console_params: dict
        :return: None
        """
        exit_code = 0
        try:
            self.console_parser.prepare_command_and_params(console_params)
            parsed_command_and_params = self.console_parser.get_parsed_command_and_params()
            if not (parsed_command_and_params is None or isinstance(parsed_command_and_params, dict)):
                raise Exception(self.cm["INCORRECT_COMMAND"])
            self.handle_command(parsed_command_and_params["path"], parsed_command_and_params["params"] if "params" in parsed_command_and_params else None)
        except ConsoleCommandError as e:
            try:
                self.helper.print_color_text(str(e), "RED")
                exit_code = e.exit_code
            finally:
                e = None
                del e

        except Exception as e:
            try:
                self.helper.print_color_text(str(e), "RED")
            finally:
                e = None
                del e

        else:
            return exit_code

    @log_method
    def handle_command(self, command, params=None):
        """
        A method to receive a request to a server and get proper handler for that request
        :param command: str;
        :param params: json or None
        :return: dict; request"s result
        """
        try:
            handler = self.get_command_handler(command)
            if handler is None:
                raise Exception(self.cm["EMPTY_MESSAGE_HANDLER"].format(str(command), "" if params is None else "with params {0}".format(str(params))))
            elif params is not None:
                handler(params)
            else:
                handler()
        except ConsoleCommandError as e:
            try:
                raise ConsoleCommandError(self.cm["FAILED_HANDLE_COMMAND"].format(str(e)), e.exit_code)
            finally:
                e = None
                del e

        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_HANDLE_COMMAND"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_command_handler(self, command):
        """
        A method contains a hub of request"s handlers.
        It returns a required handler by a request"s path or None if a handler is not find
        :param command: str;
        :return: method or None
        """
        hub = {(REQUEST_PATH_CONSTS["registerAgent"]): (self.register_agent), 
         (REQUEST_PATH_CONSTS["updateAgent"]): (self.update_agent), 
         (REQUEST_PATH_CONSTS["setAgentActivity"]): (self.deactivate_agent), 
         (REQUEST_PATH_CONSTS["saveDBMSConnection"]): (self.add_dbms_connection), 
         (REQUEST_PATH_CONSTS["updateAgentConnection"]): (self.update_dbms_connection), 
         (REQUEST_PATH_CONSTS["getAgentConnection"]): (self.get_agent_connection), 
         (REQUEST_PATH_CONSTS["testAgentConnection"]): (self.check_agent_connection), 
         (REQUEST_PATH_CONSTS["removeAgentConnection"]): (self.remove_agent_connection), 
         (REQUEST_PATH_CONSTS["listJobs"]): (self.list_jobs), 
         (REQUEST_PATH_CONSTS["runJob"]): (self.run_job), 
         (REQUEST_PATH_CONSTS["showConsoleCommands"]): (self.show_console_commands), 
         (REQUEST_PATH_CONSTS["getAppVersion"]): (self.get_app_version), 
         (REQUEST_PATH_CONSTS["uploadLogs"]): (self.upload_logs), 
         (REQUEST_PATH_CONSTS["setAppLogs"]): (self.set_logging), 
         (REQUEST_PATH_CONSTS["getInfo"]): (self.get_info), 
         (REQUEST_PATH_CONSTS["updateApp"]): (self.update_package), 
         (REQUEST_PATH_CONSTS["restartService"]): (self.restart_service), 
         (REQUEST_PATH_CONSTS["uploadDb"]): (self.upload_local_db), 
         (REQUEST_PATH_CONSTS["configureMysql"]): (self.configure_mysql), 
         (REQUEST_PATH_CONSTS["stopService"]): (self.stop_service), 
         (REQUEST_PATH_CONSTS["checkReadyToStart"]): (self.checK_ready_to_start), 
         (REQUEST_PATH_CONSTS["runJobCollector"]): (self.run_job_collector), 
         (REQUEST_PATH_CONSTS["runSubservice"]): (self.run_subservice), 
         (REQUEST_PATH_CONSTS["interactiveMenu"]): (self.run_interactive_menu)}
        if command in hub:
            return hub[command]

    @log_method
    def register_agent(self, params):
        """
        Method checks if agent already created locally
        If agent already created then check agent info. If not then create new agent
        :param params: dict with a secret-key and a computer name
        :return: dict with a message
        """
        try:
            agent = self.local_db.get_current_agent()
            agent_name = self.get_agent_name(agent, params)
            agent_version = self.get_client_version(agent)
            if agent is not None:
                if agent["AgentKey"] is not None:
                    res = self.remote_request.get_agent_info(params["key"], agent["AgentKey"])
                    if res["IsSuccess"]:
                        if res["Data"] is not None:
                            self.activate_agent(res["Data"], agent_name, agent)
                        else:
                            self.connect_agent_to_new_remote_account(params["key"], agent, agent_name, agent_version)
                    else:
                        self.connect_agent_to_new_remote_account(params["key"], agent, agent_name, agent_version)
                else:
                    self.create_new_agent(params, agent_name, agent_version)
            else:
                reload_global_config()
                if params["skip-interactive-add-connection"] != "y":
                    self.helper.print_color_text("")
                    self.helper.print_color_text("_________________________________________________________")
                    self.helper.print_color_text("")
                    self.helper.print_color_text("To make backups, sqlbak needs to connect to the database.", CONSOLE_COLORS["WHITE"])
                    add_database_menu()
                else:
                    is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
                host_name = self.helper.get_host_name()
                msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
                self.helper.print_color_text(self.cm["CREATE_DBMS_CONNECTION_1"].format(msg_param))
                self.helper.print_color_text(self.cm["CREATE_DBMS_CONNECTION_2"].format(msg_param), CONSOLE_COLORS["GREY"])
                self.helper.print_color_text(self.cm["CREATE_DBMS_CONNECTION_3"].format(msg_param), CONSOLE_COLORS["GREY"])
        except KeyboardInterrupt:
            pass
        except ConsoleCommandError as e:
            try:
                raise ConsoleCommandError(self.cm["FAILED_REG_CLIENT"].format(str(e)), e.exit_code)
            finally:
                e = None
                del e

        except Exception as e:
            try:
                raise ConsoleCommandError(self.cm["FAILED_REG_CLIENT"].format(str(e)), 1)
            finally:
                e = None
                del e

    @log_method
    def get_agent_name(self, current_agent, params):
        """
        Try to get an agent name
        :param current_agent:
        :param params:
        :return: agent_name (str)
        """
        if "name" in params and params["name"] is None:
            agent_name = current_agent["AgentName"] if current_agent is not None else socket.gethostname()
        else:
            agent_name = params["name"]
        return str(agent_name.strip())[0[:64]]

    @log_method
    def get_client_version(self, agent):
        """
        a method to get a current client version
        :param agent: dict
        :return: client version (dict)
        """
        if agent is not None:
            app_version = [
             agent["MajorVersion"], agent["MinorVersion"], agent["PatchVersion"]]
        else:
            app_version = CONFIG["APP_VERSION"].split(".")
        if len(app_version) < 3:
            raise Exception(self.cm["FAILED_GET_VERSION"])
        return {'major_version':app_version[0], 
         'minor_version':app_version[1], 
         'patch_version':app_version[2]}

    @log_method
    def activate_agent(self, remote_agent, agent_name, current_agent):
        """
        A method to update agent activity at a remote server and at a local database
        :param remote_agent: string
        :param agent_name: string
        :param current_agent: string
        :return: None
        """
        self.local_db.update_down_alert_interval(remote_agent["Profile"]["Plan"]["CheckTimeout"])
        if remote_agent["IsActive"]:
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            raise ConsoleCommandError(self.cm["COMP_CONNECTED"].format(remote_agent["AccountName"], remote_agent["AgentName"], msg_param), 101)
        result = self.remote_request.set_agent_activity(current_agent["AgentKey"], True)
        if not result["IsSuccess"]:
            raise ConsoleCommandError(self.cm["FAILED_ACTIVATE_CLIENT"].format(str(result["ErrorMessage"])), 102)
        self.local_db.update_agent_activity(current_agent["AgentKey"], 1)
        self.helper.print_color_text(self.cm["SUCCESSFUL_CONNECTED"].format(agent_name, remote_agent["AccountName"]))
        if agent_name != remote_agent["AgentName"]:
            self.update_agent_name(current_agent, remote_agent["AgentName"])

    @log_method
    def update_agent_name(self, agent, agent_name):
        """
        A method to update agent name
        :param agent:
        :param agent_name:
        :return:
        """
        result_update_agent = self.remote_request.update_agent_name(agent["AgentKey"], agent["AgentId"], agent_name)
        if not result_update_agent["IsSuccess"]:
            raise Exception(self.cm["FAILED_UPDATE_NAME"].format(str(result_update_agent["ErrorMessage"])))
        self.local_db.update_agent_name(agent["AgentKey"], agent_name)
        self.helper.print_color_text(self.cm["NEW_CLIENT_NAME"].format(agent_name))

    @log_method
    def connect_agent_to_new_remote_account(self, secret_key, current_agent, computer_name, app_version):
        """
        A method to connect a current agent to another remote account
        :param secret_key: string
        :param current_agent: string
        :param computer_name: string
        :param app_version: dict
        :return: None
        """
        if current_agent["AgentKey"] is not None:
            result_activation = self.remote_request.set_agent_activity(current_agent["AgentKey"], False)
            if not result_activation["IsSuccess"]:
                raise Exception(self.cm["FAILED_SET_AGENT_ACTIVITY"].format(str(result_activation["ErrorMessage"])))
        utils_path = json.loads(current_agent["UtilsPath"])
        session_id = self.helper.get_uuid()
        new_agent = self.register_new_agent(secret_key, computer_name, utils_path, app_version, session_id)
        self.local_db.delete_all_client_records()
        self.local_db.update_agent(new_agent["AgentKey"], new_agent["AgentId"], new_agent["AgentName"], new_agent["AccountName"], new_agent["IsActive"], new_agent["Profile"]["WorkingDir"], session_id)
        self.helper.print_color_text(self.cm["SUCCESSFUL_CONNECTED"].format(computer_name, new_agent["AccountName"]))

    @log_method
    def create_new_agent(self, params, computer_name, app_version):
        """
        A method to create a new agent with passed computer name and utils path
        :param params: dict
        :param computer_name: string
        :param app_version: dict
        :return: None
        """
        register_app(params["key"], computer_name)
        agent = self.local_db.get_current_agent()
        self.helper.print_color_text(self.cm["SUCCESSFUL_CONNECTED"].format(computer_name, agent["AccountName"]))

    @log_method
    def register_new_agent(self, secret_key, computer_name, utils_path, app_version, session_id):
        return register_new_agent_on_the_sqlbak_server(secret_key, computer_name, utils_path, app_version, session_id)

    @log_method
    def update_agent(self, params):
        """
        A method to update computer name on a remote server and in local db
        if a passed computer name different from a current name
        :param params: dict
        :return: None
        """
        try:
            agent = self.local_db.get_current_agent()
            if not agent is None:
                raise agent["IsActive"] or Exception(self.cm["UNREGISTERED_COMP"])
            else:
                agent_name = self.get_agent_name(agent, params)
                if agent_name != agent["AgentName"]:
                    self.update_agent_name(agent, agent_name)
                else:
                    self.helper.print_color_text(self.cm["COMP_NAME_UNCHANGED"].format(agent_name))
            self.update_agent_utils_path(agent, params)
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_UPDATE_CLIENT"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def update_agent_utils_path(self, agent, params):
        """
        A method to update agent utils path
        :param agent: dict
        :param params: dict
        :return: none
        """
        current_utils_path = json.loads(agent["UtilsPath"])
        new_utils_path = {
         'mysqldump-path': None, 
         'mysql-path': None, 
         'mysql-binlog-base-path': None, 
         'mysql-binlog-index-path': None, 
         'pgdump-path': None, 
         'psql-path': None, 
         'sqlcmd-path': None, 
         'mssql-data': None, 
         'xtrabackup-path': None, 
         'mysql-lib': None, 
         'mongo-path': None, 
         'mongodump-path': None, 
         'mongorestore-path': None, 
         'pg_restore-path': None, 
         'sqlpackage-path': None}
        changed = False
        for key in new_utils_path:
            if params[key] is None:
                if key in current_utils_path:
                    new_utils_path[key] = current_utils_path[key]
                else:
                    new_utils_path[key] = AGENT_UTILS_PATH[key]
            else:
                changed = True
                new_utils_path[key] = params[key]
        else:
            agent["SessionId"] = self.helper.update_agent_session(agent, self.local_db)
            result_request = self.remote_request.update_agent(agent, new_utils_path)
            if not result_request["IsSuccess"]:
                raise Exception(self.cm["FAILED_UPDATE_PATHS"].format(str(result_request["ErrorMessage"])))
            self.local_db.update_agent_utils_path(agent["AgentKey"], new_utils_path)
            if changed:
                self.helper.print_color_text(self.cm["UTILS_PATH_CHANGED"].format(str(new_utils_path)))

    @log_method
    def deactivate_agent(self):
        """
        A method to deactivate agent
        :return: dict with a message
        """
        try:
            unregister_app()
            self.helper.print_color_text(self.cm["UNREGISTERED_COMP"])
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_DEACTIVATE_CLIENT"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def add_dbms_connection(self, params):
        self.connection.add_dbms_connection(params)

    @log_method
    def update_dbms_connection(self, params):
        self.connection.update_dbms_connection(params)

    @log_method
    def get_agent_connection(self, params):
        self.connection.get_agent_connection(params)

    @log_method
    def check_agent_connection(self, params):
        self.connection.check_agent_connection(params)

    @log_method
    def remove_agent_connection(self, params):
        self.connection.remove_agent_connection(params)

    @log_method
    def list_jobs(self, params):
        """
        Method to get and show a list of existing jobs
        :return: None
        """
        try:
            if self.local_db.get_current_agent() is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            else:
                jobs_list = self.local_db.get_list_of_jobs()
                if jobs_list is None:
                    raise Exception(self.cm["NO_JOBS"])
                messages = self.get_jobs_messages(jobs_list)
                if "--text-only" in params and params["--text-only"] == "yes":
                    self.helper.print("\n".join(messages))
                else:
                    self.helper.print_color_text("\n".join(messages))
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_GET_JOBS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_jobs_messages(self, jobs_list):
        messages = []
        for job in jobs_list:
            connection = self.local_db.get_connection_by_job_cred_id(job["JobCredentialsId"])
            if connection is None:
                pass
            else:
                messages.append("Job-Id: {0}, Job-Name: {1}, Connection-Id: {2}, DBMS-Type: {3}, Connection-Name: {4}".format(job["JobId"], job["JobName"], connection["ConnectionId"], connection["ServerType"], connection["ConnectionName"]))
        else:
            return messages

    @log_method
    def run_job(self, job):
        """
        A method to run a job
        :param job: dict
        :return: None
        """
        try:
            jobs_list = "job-id" in job and job["job-id"] or self.local_db.get_list_of_jobs()
            if jobs_list is None or len(jobs_list) == 0:
                raise Exception(self.cm["FAILD_RUN_JOB_BY_NAME_NO_ANY_JOBS"])
            elif "job-name" in job:
                if job["job-name"]:
                    jobName = job["job-name"].strip("'").strip('"')
                    findedJobs = [x["JobId"] for x in jobs_list if x["JobName"] == jobName]
                    if len(findedJobs) == 0:
                        raise Exception(self.cm["FAILD_RUN_JOB_BY_NAME_NO_FOUND"].format(jobName, [x["JobName"] for x in jobs_list]))
                    else:
                        if len(findedJobs) > 1:
                            raise Exception(self.cm["FAILD_RUN_JOB_BY_NAME_MORE_ONE_JOB_WITH_NAME"].format(jobName))
                        else:
                            job_id = str(findedJobs[0])
                else:
                    if len(jobs_list) > 1:
                        raise Exception(self.cm["FAILD_RUN_JOB_BY_NAME_NEED_NAME"].format(jobs_list[0]["JobName"], [x["JobName"] for x in jobs_list]))
                    else:
                        job_id = str(jobs_list[0]["JobId"])
            else:
                job_id = job["job-id"]
            is_success_job = self.plain_job.run_job({'JobId':job_id, 
             'JobBackupType':job["backup-type"].upper() if ("backup-type" in job) else FULL_BACKUP_CONST, 
             'JobMode':BACKUP_JOB_MODE["CLI"], 
             'JobInfo':None, 
             'MessageId':None, 
             'SendMessage':None, 
             'Message':None, 
             'IsConsoleMode':True})
            if not is_success_job:
                raise ConsoleCommandError("", 1)
        except ConsoleCommandError as e1:
            try:
                raise e1
            finally:
                e1 = None
                del e1

        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_RUN_JOB"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def show_console_commands(self, params):
        self.console_parser.show_console_commands(params)

    @log_method
    def get_app_version(self):
        year_ = date.today().year
        app_years = str("2019-" + str(year_) if year_ > 2019 else year_)
        self.helper.print_color_text(self.cm["CURRENT_CLIENT_VERSION"].format(CONFIG["APP_VERSION"], app_years))

    @log_method
    def upload_logs(self):
        try:
            upload = UploadAppLogs()
            upload.upload_app_logs_to_server()
            self.helper.print_color_text(self.cm["LOGS_UPLOADED"])
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_UPLOAD_LOGS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def set_logging(self, params):
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            is_logging_activated = True if params["activate"].lower() == "y" else False
            self.helper.update_dynamic_settings_property(DYNAMIC_SETTING_LOGGING_ACTIVATED, str(is_logging_activated))
            self.helper.print_color_text(self.cm["LOGGING_STATUS"].format("activated" if is_logging_activated else "deactivated"))
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_ACTIVATE_LOGS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_info(self):
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            is_active = self.is_agent_active(agent)
            self.update_agent_if_activity_changed(agent, is_active)
            self.print_agent_info(agent, is_active)
            self.print_agent_utils(agent["UtilsPath"])
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_GET_CLIENT_INFO"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def is_agent_active(self, agent):
        request_result = self.remote_request.get_agent_status(agent["AgentKey"])
        if not request_result["IsSuccess"]:
            raise Exception(str(request_result["ErrorMessage"]))
        return request_result["Data"]["IsActive"]

    @log_method
    def update_agent_if_activity_changed(self, agent, is_active):
        if int(is_active) != int(agent["IsActive"]):
            self.local_db.update_agent_activity(agent["AgentKey"], int(is_active))

    @log_method
    def print_agent_info(self, agent, is_active):
        is_agent_activated = self.helper.is_text_true(self.helper.get_dynamic_settings_value(DYNAMIC_SETTING_LOGGING_ACTIVATED))
        self.helper.print_color_text(self.cm["CLIENT_INFO"].format(str(agent["AgentName"]), agent["AccountName"], "registered" if int(is_active) else "unregistered", "activated" if is_agent_activated else "deactivated"))

    @log_method
    def print_agent_utils(self, utils_path):
        utils = json.loads(utils_path)
        for u in utils:
            if AGENT_UTILS_PATH[u] != utils[u]:
                self.helper.print_color_text(u + ": " + utils[u])

    @log_method
    def update_package(self):
        u_app = UpdateApp()
        u_app.update_package(mode=(UPDATE_APP_SOURCES["MANUALLY"]))

    @log_method
    def restart_service(self):
        trace_app_message("The service was restarted using a cron task.")

    @log_method
    def stop_service(self):
        update_app = UpdateApp()
        update_app.stop_service()

    @log_method
    def checK_ready_to_start(self):
        agent = self.local_db.get_current_agent()
        if agent is None:
            raise ConsoleCommandError(self.cm["UNREGISTERED_COMP"], 1)
        if self.local_db.get_connections_by_server_type("all") is None:
            raise ConsoleCommandError(self.cm["NO_ANY_CONNECTIONS"], 1)

    @log_method
    def run_job_collector(self):
        cleanup_lost_backup_logs(Job())

    def run_subservice(self, params):
        app = App()
        app.__getattribute__(params["service-name"])()

    def run_interactive_menu(self):
        main_menu()

    @log_method
    def upload_local_db(self):
        upload = UploadAppLogs()
        upload.upload_local_db()

    @log_method
    def configure_mysql(self, params):
        agent = self.local_db.get_current_agent()
        if agent is None:
            raise Exception(self.cm["UNREGISTERED_COMP"])
        else:
            connection = self.local_db.get_connection_by_id(params["connection-id"])
            if connection is None:
                self.helper.print_color_text(self.cm["CONNECTION_NOT_FOUND"].format(params["connection-id"]), CONSOLE_COLORS["RED"])
            else:
                connection_params = self.connection.get_connection_params_to_test(connection, agent)
                dbms = DBMS(connection_params)
                instance = dbms.get_db_server_class_instance()
                row_format = instance.is_row_format_enabled()
                is_bin_log_enabled = instance.is_bin_log_enabled()
                if is_bin_log_enabled:
                    if row_format:
                        self.helper.print_color_text(self.cm["CORRECT_BIN_LOG_SETTINGS"], CONSOLE_COLORS["GREEN"])
                    else:
                        self.helper.print_color_text(self.cm["WRONG_BIN_LOG_PARAMS"], CONSOLE_COLORS["RED"])
                else:
                    txt = input(self.cm["ACTIVATE_BIN_LOGS"])
                    instance.handle_user_enter(txt)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/console_handler.pyc
