from sqlbak.local_db import LocalDB
from sqlbak.helper import Helper
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.definitions import CONSOLE_COLORS, AVAILABLE_SERVER_TYPES, CONFIG, DBMS_TYPES_CONSTS, PORTS_SCOPE, XTRABACKUP_CONST, SUDO_SQLBAK, DOCKER_EXEC
from sqlbak.console_parser import ConsoleParser
from sqlbak.dbms.dbms import DBMS
from sqlbak.app_output import APP_OUTPUT
from sqlbak.logger import log_method
import os
import xml.etree.ElementTree as Et
import json

class Connection:

    def __init__(self):
        self.helper = Helper()
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
        self.console_parser = ConsoleParser()

    @log_method
    def add_dbms_connection(self, params):
        """
        Method to add new DBMS connection
        :param params: dict;
        :return: dict;
        """
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            params["db-type"] = params["db-type"].lower()
            if params["db-type"] not in DBMS_TYPES_CONSTS:
                raise Exception(self.cm["WRONG_SERVER_TYPE"].format(params["db-type"], ", ".join(AVAILABLE_SERVER_TYPES)))
            params["port"] = self.get_connection_port(params)
            if not self.is_port_number_lay_in_correct_score(params["port"]):
                raise Exception(self.cm["INCORRECT_PORT_SCOPE"].format(params["port"], PORTS_SCOPE))
            settings = self.update_passed_connection_params(params)
            params["connection-name"] = settings["ConnectionName"]
            connection_params = self.get_connection_params_to_test(settings, agent)
            self.advanced_check_dbms_utils(params["db-type"])
            res = self.test_agent_connection(connection_params)
            if not res["is_success"]:
                raise Exception(res["error"])
            server_type_value = self.helper.get_dbms_type_by_name(params["db-type"], params["connection-type"])
            version = 1
            credential_id = self.save_connection_name_at_remote_server(agent["AgentKey"], server_type_value, params["connection-name"], version)
            params["connection-id"] = self.save_agent_connection(params, credential_id, settings["BackupUtil"])
            message = ("Connection-Id: {connection-id}, DBMS-Type: {db-type}, Connection-Name: {connection-name}".format)(**params)
            if "should_print_result" not in params or params["should_print_result"]:
                self.helper.print_color_text(" ".join([self.cm["CONNECTION_ADDED"], message, self.cm["LEAD_TO_THE_SITE_AFTER_CONNECTION"]]))
            return             return credential_id
            except Exception as e:
            try:
                error = self.get_error_description(str(e), params["db-type"])
                raise Exception(self.cm["FAILED_ADD_CONNECTION"].format(error))
            finally:
                e = None
                del e

    @log_method
    def is_port_number_lay_in_correct_score(self, port):
        return int(port) in range(PORTS_SCOPE[0], PORTS_SCOPE[1])

    def get_connection_data_by_id(self, connection_id):
        """
        Method to get connection data by id
        :param connection_id: int;
        :return: dict;
        """
        return self.local_db.get_connection_by_id(connection_id)

    @log_method
    def update_dbms_connection(self, params):
        """
        A method to update a DBMS connection
        :param params: dict
        :return: None
        """
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            connection = self.local_db.get_connection_by_id_with_alias_params(params["connection-id"])
            if connection is None:
                raise Exception(self.cm["CONNECTION_NOT_FOUND"].format(params["connection-id"]))
            res = self.console_parser.parse_connection_params(connection, params)
            updated_params = res["updated_params"]
            updated_params["Version"] = int(connection["Version"]) + 1
            if updated_params["ServerType"] not in AVAILABLE_SERVER_TYPES:
                raise Exception(self.cm["WRONG_SERVER_TYPE"].format(updated_params["ServerType"], ", ".join(AVAILABLE_SERVER_TYPES)))
            connection_params = self.get_connection_params_to_test(updated_params, agent)
            if not self.is_port_number_lay_in_correct_score(connection_params["Port"]):
                raise Exception(self.cm["INCORRECT_PORT_SCOPE"].format(connection_params["Port"], PORTS_SCOPE))
            res = self.test_agent_connection(connection_params)
            if not res["is_success"]:
                raise Exception(res["error"])
            params_for_connection_name = {'Host':connection_params["Host"], 
             'Port':connection_params["Port"], 
             'UseSsh':updated_params["UseSsh"], 
             'SshHost':updated_params["SshHost"], 
             'SshPort':updated_params["SshPort"]}
            updated_params = self.get_updated_connection_params(updated_params, params_for_connection_name, params["connection-id"], agent)
            message = ("Connection-Id: {ConnectionId}, DBMS-Type: {ServerType}, Connection-Name: {ConnectionName}".format)(**updated_params)
            if "should_print_result" not in params or params["should_print_result"]:
                self.helper.print_color_text(" ".join([self.cm["CONNECTION_UPDATED"], message]))
            return             return connection["ConnCredentialId"]
            except Exception as e:
            try:
                error = self.get_error_description(str(e), params["db-type"])
                raise Exception(self.cm["FAILED_UPDATE_CONNECTION"].format(error))
            finally:
                e = None
                del e

    @log_method
    def save_agent_connection(self, params, credential_id, backup_util):
        connection_id = self.local_db.add_connection(params["db-type"], params["connection-type"], params["host"], params["port"], params["user"], params["password"], params["use-ssh"], params["ssh-host"] if "ssh-host" in params else None, params["ssh-port"], params["ssh-local-mapped-port"], params["ssh-user"] if "ssh-user" in params else None, params["ssh-password"] if "ssh-password" in params else None, params["connection-name"], int(credential_id), backup_util, params["database"])
        return connection_id

    @log_method
    def get_connection_port(self, params):
        if "port" not in params or params["port"] is None:
            params["port"] = DBMS_TYPES_CONSTS[params["db-type"]]["default_port"]
        return params["port"]

    @log_method
    def update_passed_connection_params(self, params):
        ssh_part = self.get_ssh_connection_settings(params)
        return {'ServerType':params["db-type"], 
         'ConnectionType':params["connection-type"], 
         'Host':params["host"], 
         'Port':params["port"], 
         'User':params["user"], 
         'Password':self.helper.encrypt_string(params["password"]) if (params["password"]) else None, 
         'UseSsh':params["use-ssh"], 
         'SshHost':params["ssh-host"] if ("ssh-host" in params) else None, 
         'SshPort':params["ssh-port"], 
         'SshLocalMappedPort':params["ssh-local-mapped-port"], 
         'SshUser':params["ssh-user"] if ("ssh-user" in params) else None, 
         'SshPassword':self.helper.encrypt_string(params["ssh-password"]) if ("ssh-password" in params) else None, 
         'ConnectionName':(ssh_part + params["host"] + ":") + (str(params["port"])), 
         'BackupUtil':None, 
         'Database':params["database"]}

    def extract_connection_params(self, updated_params):
        params = {'db-type':updated_params["ServerType"], 
         'connection-type':updated_params["ConnectionType"], 
         'host':updated_params["Host"], 
         'port':updated_params["Port"], 
         'user':updated_params["User"], 
         'password':self.helper.decrypt_string(updated_params["Password"]) if (updated_params["Password"]) else None, 
         'use-ssh':updated_params["UseSsh"], 
         'ssh-host':updated_params["SshHost"], 
         'ssh-port':updated_params["SshPort"], 
         'ssh-local-mapped-port':updated_params["SshLocalMappedPort"], 
         'ssh-user':updated_params["SshUser"], 
         'ssh-password':self.helper.decrypt_string(updated_params["SshPassword"]) if (updated_params["SshPassword"]) else None, 
         'database':updated_params["Database"]}
        return params

    @log_method
    def get_backup_util(self, params):
        backup_util = params["backup-util"]
        if params["db-type"] == XTRABACKUP_CONST:
            if backup_util == XTRABACKUP_CONST:
                backup_util = XTRABACKUP_CONST
            else:
                raise Exception(self.cm["WRONG_BACKUP_UTIL"])
        else:
            backup_util = None
        return backup_util

    @log_method
    def get_updated_connection_params(self, params, params_for_connection_name, connection_id, agent):
        connection_name = self.get_connection_name(params_for_connection_name)
        if params["ConnectionName"] != connection_name:
            server_type_value = self.helper.get_dbms_type_by_name(params["ServerType"], params["ConnectionType"])
            credential_id = self.save_connection_name_at_remote_server(agent["AgentKey"], server_type_value, connection_name, params["Version"], params["ConnCredentialId"])
            params["ConnCredentialId"] = credential_id
            params["ConnectionName"] = connection_name
        self.local_db.update_connection_params(connection_id, params)
        return params

    @log_method
    def get_connection_name(self, params):
        ssh_part = ""
        if int(params["UseSsh"]):
            ssh_part = "SSH://" + str(params["SshHost"]) + ":" + str(params["SshPort"]) + "/"
        return ssh_part + str(params["Host"]) + ":" + str(params["Port"])

    @log_method
    def get_ssh_connection_settings(self, params):
        ssh_part = ""
        if params["use-ssh"]:
            ssh_part = "SSH://" + params["ssh-host"] + ":" + str(params["ssh-port"]) + "/"
        return ssh_part

    @log_method
    def update_connection_name(self, agent_key, server_type, connection_type, connection_name):
        """
        A method to update a connection name at remote server
        :param agent_key: str
        :param server_type: int
        :param connection_type: str
        :param connection_name: str
        :param credential_id: int or None
        :return: False or credential id (int)
        """
        server_type_value = self.helper.get_dbms_type_by_name(server_type, connection_type)
        connection = self.local_db.get_connection_by_server_type_and_connection_name(server_type, connection_name)
        if connection is not None:
            message = ("Connection-Id: {ConnectionId}, DBMS-Type: {ServerType}, Connection-Name: {ConnectionName}".format)(**connection)
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            raise Exception(" ".join([self.cm["DOUBLE_CONNECTION"].format(msg_param), message]))

    @log_method
    def save_connection_name_at_remote_server(self, agent_key, server_type_value, connection_name, version, credential_id=None):
        res = self.remote_request.save_job_credentials(agent_key, server_type_value, connection_name, version, credential_id)
        if not res["IsSuccess"]:
            raise Exception(self.cm["SAVE_AGENT_NAME_FAILED"].format(str(res["ErrorMessage"])))
        return res["Data"]

    @log_method
    def advanced_check_dbms_utils(self, db_type):
        if db_type == "azure":
            error_message = ""
            utils_path = json.loads(self.local_db.get_current_agent()["UtilsPath"])
            if not os.path.exists(utils_path["sqlpackage-path"]):
                error_message += self.cm["MISSED_SQLPACKAGE_UTIL"].format(utils_path["sqlpackage-path"])
            if not os.path.exists(utils_path["sqlcmd-path"]):
                error_message += self.cm["MISSED_SQLCMD_UTIL"].format(utils_path["sqlcmd-path"])
            if error_message:
                error_message = "\n" + error_message
                raise Exception(error_message)

    @log_method
    def get_error_description(self, error, db_type):
        if "not found" in error:
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            error_description = self.cm["MISSED_DBMS_UTIL"].format(DBMS_TYPES_CONSTS[db_type]["client_util"], DBMS_TYPES_CONSTS[db_type]["default_path"], DBMS_TYPES_CONSTS[db_type]["default_util"], msg_param)
            error += "\n{0}".format(error_description)
        return error

    @log_method
    def get_messages_to_print_connections(self, connections):
        messages = []
        for c in connections:
            messages.append(("Connection-Id: {ConnectionId}, DBMS-Type: {ServerType}, Connection-Name: {ConnectionName}".format)(**c))
        else:
            return messages

    @log_method
    def get_agent_connection(self, params):
        """
        Method to get a client"s connection
        :param params: dict;
        :return: dict;
        """
        try:
            if self.local_db.get_current_agent() is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            else:
                connection_id = params.get("connection-id", None)
                db_type = params.get("db-type", "all")
                if connection_id is not None:
                    self.get_connection_by_id(connection_id)
                else:
                    self.get_connections_by_dbms_type(db_type)
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_GET_CONNECTIONS"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def get_connection_by_id(self, connection_id):
        connection = self.local_db.get_connection_by_id(connection_id)
        if connection is None:
            self.helper.print_color_text(self.cm["CONNECTION_NOT_FOUND"].format(connection_id), CONSOLE_COLORS["RED"])
        else:
            self.helper.print_color_text(("Connection-Id: {ConnectionId}, DBMS-Type: {ServerType}, Connection-Name: {ConnectionName}, Host: {Host}, Port: {Port}, User: {User}, Use-SSH: {UseSsh}, SSH-Host: {SshHost}, SSH-Port: {SshPort}, SSH-Local-Mapped-Port: {SshLocalMappedPort}, SSH-User: {SshUser}, BackupUtil: {BackupUtil}".format)(**connection))

    @log_method
    def get_connections_by_dbms_type(self, db_type):
        if db_type in DBMS_TYPES_CONSTS.keys() or db_type == "all":
            connections = self.local_db.get_connections_by_server_type(db_type)
            if connections is None:
                self.helper.print_color_text(self.cm["NO_CONNECTIONS"].format("" if db_type == "all" else "to " + db_type))
                return
            messages = self.get_messages_to_print_connections(connections)
            self.helper.print_color_text("\n".join(messages))
            return connections
        else:
            self.helper.print_color_text(self.cm["WRONG_SERVER_TYPE"].format(db_type, ", ".join(DBMS_TYPES_CONSTS.keys())), CONSOLE_COLORS["RED"])
            return

    @log_method
    def check_agent_connection(self, params):
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            connection = self.local_db.get_connection_by_id(params["connection-id"])
            if connection is None:
                raise Exception(self.cm["CONNECTION_NOT_FOUND"].format(params["connection-id"]))
            params.update(connection)
            connection_params = self.get_connection_params_to_test(params, agent)
            res = self.test_agent_connection(connection_params)
            self.print_test_connection_result(connection_params, res)
        except Exception as e:
            try:
                error = self.helper.get_knowledge_base_error(str(e))
                raise Exception(self.cm["FAILED_TEST_CONNECTION"].format(error))
            finally:
                e = None
                del e

    @log_method
    def test_agent_connection(self, connection_params):
        """
        Method to test client"s connection
        :param params: dict;
        :param should_raise_exception: bool;
        :return: None
        """
        dbms = DBMS(connection_params)
        return dbms.test_db_connection()

    @log_method
    def get_connection_params_to_test(self, params, agent):
        connection_params = {'UtilsPath':agent["UtilsPath"], 
         'My_PasswordInEnv':True}
        connection_params.update(params)
        return connection_params

    @log_method
    def print_test_connection_result(self, connection, test_result):
        self.helper.print_color_text("Connection-Id: %(ConnectionId)s, DBMS-Type: %(ServerType)s, Connection-Name: %(ConnectionName)s" % connection)
        if test_result["is_success"]:
            self.helper.print_color_text(self.cm["TEST_CONNECTION_SUCCESS"])
        else:
            self.helper.print_color_text(self.cm["TEST_CONNECTION_FAILED"].format(test_result["error"]), CONSOLE_COLORS["RED"])

    def get_jobs_by_connection_id(self, connection_id):
        """
        Method to get jobs by connection id
        :param connection_id: str;
        :return: list;
        """
        connection = self.local_db.get_connection_by_id(connection_id)
        if connection is None:
            raise Exception(self.cm["CONNECTION_NOT_FOUND"].format(connection_id))
        return self.local_db.get_jobs_by_credentials_id(connection["ConnCredentialId"])

    @log_method
    def remove_agent_connection(self, params, should_print=True, force=False):
        """
        Method to remove client"s connection from a remote server and from local db
        :param params: dict;
        :return: None;
        """
        try:
            agent = self.local_db.get_current_agent()
            if agent is None:
                raise Exception(self.cm["UNREGISTERED_COMP"])
            connection = self.local_db.get_connection_by_id(params["connection-id"])
            if connection is None:
                raise Exception(self.cm["CONNECTION_NOT_FOUND"].format(params["connection-id"]))
            if not force:
                jobs = self.local_db.get_jobs_by_credentials_id(connection["ConnCredentialId"])
                if jobs is not None:
                    raise Exception(self.cm["DELETE_CONNECTION_FAILED"].format(str(len(jobs))))
            res = self.remote_request.delete_job_credentials(agent["AgentKey"], connection["ConnCredentialId"])
            if not res["IsSuccess"]:
                raise Exception(self.cm["FAILED_REMOVE_JOB_CRED"].format(str(res["ErrorMessage"])))
            self.local_db.delete_connection_by_id(params["connection-id"])
            self.local_db.delete_dbms_connection_state_by_connection_id(params["connection-id"])
            if should_print:
                self.print_remove_connection_messages(params, connection)
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_REMOVE_CONNECTION"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def print_remove_connection_messages(self, params, connection):
        message = "Connection-Id: {0}".format(params["connection-id"])
        message += "\n" + self.cm["CONNECTION_DELETED"]
        self.helper.print_color_text(message)

    @log_method
    def get_dbms_connection_settings(self, json_data):
        connection_settings = Et.fromstring(json_data["Settings"].encode("utf-16"))
        job_credential_id = json_data["JobCredentialsId"] if "JobCredentialsId" in json_data else None
        if int(json_data["ServerType"]) == 4:
            port_param = "MySqlPort"
            host = "SqlServerHost"
            user = "UserName"
        else:
            if int(json_data["ServerType"]) == 1:
                port_param = "MsSqlPort"
                host = "Server"
                user = "UserName"
            else:
                if int(json_data["ServerType"]) == 9:
                    port_param = "Port"
                    host = "Host"
                    user = "User"
                else:
                    if int(json_data["ServerType"]) == 2:
                        port_param = "Port"
                        host = "Server"
                        user = "UserName"
                    else:
                        user = "Login"
                        host = "Server"
                        port_param = "Port"
        return {'db-type':(self.helper.get_dbms_name_by_server_type)(int(json_data["ServerType"])), 
         'port':connection_settings.attrib[port_param] if (port_param in connection_settings.attrib) else None, 
         'connection-name':"", 
         'connection-type':"tcp/ip", 
         'host':connection_settings.attrib[host], 
         'user':connection_settings.attrib[user] if (user in connection_settings.attrib) else None, 
         'password':connection_settings.attrib["Password"] if ("Password" in connection_settings.attrib) else None, 
         'use-ssh':self.helper.is_text_true(connection_settings.attrib["UseSsh"]) if ("UseSsh" in connection_settings.attrib) else False, 
         'ssh-host':connection_settings.attrib["SshHostname"] if ("SshHostname" in connection_settings.attrib) else None, 
         'ssh-port':connection_settings.attrib["SshPort"] if ("SshPort" in connection_settings.attrib) else None, 
         'ssh-local-mapped-port':connection_settings.attrib["SshMappedPort"] if ("SshMappedPort" in connection_settings.attrib) else None, 
         'ssh-user':connection_settings.attrib["SshUserName"] if ("SshUserName" in connection_settings.attrib) else "", 
         'ssh-password':connection_settings.attrib["SshPassword"] if ("SshPassword" in connection_settings.attrib) else "", 
         'timeout':connection_settings.attrib["Timeout"] if ("Timeout" in connection_settings.attrib) else None, 
         'test_before_save':json_data["TestBeforeSave"] if ("TestBeforeSave" in json_data) else False, 
         'path_to_bin_folder':connection_settings.attrib["PathToBinFolder"] if ("PathToBinFolder" in connection_settings.attrib) else "", 
         'should_print_result':False, 
         'job_credential_id':job_credential_id, 
         'database':connection_settings.attrib["AuthDatabaseName"] if ("AuthDatabaseName" in connection_settings.attrib) else None}

    @log_method
    def get_dbms_connection_settings_as_xml(self, server_type, dbms_connection):
        agent = self.local_db.get_current_agent()
        params = {'ServerType':server_type, 
         'UtilsPath':agent["UtilsPath"]}
        dbms = DBMS(params)
        return dbms.get_dbms_settings_as_xml(dbms_connection)

    @log_method
    def test_dbms_connection(self, data, agent):
        json_data = json.loads(data)
        dbms_connection_settings = self.get_dbms_connection_settings(json_data)
        try:
            password = self.helper.decrypt_string(dbms_connection_settings["password"])
        except Exception:
            password = dbms_connection_settings["password"]
        else:
            try:
                ssh_password = self.helper.decrypt_string(dbms_connection_settings["ssh-password"])
            except Exception:
                ssh_password = dbms_connection_settings["ssh-password"]
            else:
                dbms_connection_settings["password"] = password
                dbms_connection_settings["ssh-password"] = ssh_password
                connection_params = self.get_connection_params_to_test(dbms_connection_settings, agent)
                settings = self.update_passed_connection_params(connection_params)
                settings["UtilsPath"] = connection_params["UtilsPath"]
                res = self.test_agent_connection(settings)
                if not res["is_success"]:
                    raise Exception(res["error"])

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/connection.pyc
