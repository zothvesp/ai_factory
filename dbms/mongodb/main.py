
import os, json, re
from sqlbak.definitions import CONFIG, BACKUP_TYPES, FULL_BACKUP_CONST, SQL_SCRIPT_TYPE, CONSOLE_COLORS, SYSTEM_DATABASES_MONGO
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_method
from sqlbak.app_output import APP_OUTPUT

class MongoMain:

    @log_method
    def __init__(self, params=None):
        self.helper = Helper()
        self.params = params
        self.utils = json.loads(self.params["UtilsPath"])
        self.local_db = LocalDB()
        self.native_command = NativeCommand()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def get_params_for_request(self, command, request=''):
        params = self.helper.get_params_to_run_server_script(command, request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return params

    @log_method
    def make_tcp_request(self, command, request=''):
        params = self.helper.get_params_to_run_server_script(command, request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return self.native_command.make_tcp_request_to_mongo(params)

    @log_method
    def get_auth_database(self, database=None):
        if database is None:
            if "Database" in self.params:
                if self.params["Database"] is not None:
                    database = self.params["Database"]
        auth_database = "admin"
        if database is not None:
            auth_database = database.strip()
        return auth_database

    @log_method
    def bson_to_json(self, bson_data):
        jsondata = re.sub("NumberLong\\s*\\(\\s*(\\S+)\\s*\\)", "\\1", bson_data)
        return jsondata

    def get_mongo_cli_path(self):
        path = self.utils["mongo-path"]
        if os.path.exists(path):
            return path
        if os.path.exists(path + "sh"):
            return path + "sh"
        return path

    def eval(self, command, non_empty_result):
        cmd = ' --authenticationDatabase \'{0}\' --quiet --eval "{1}" '.format(self.get_auth_database(self.params["Database"]), command)
        result = self.make_tcp_request(self.get_mongo_cli_path(), cmd)
        if result:
            return result
        if non_empty_result:
            raise Exception('The "{0}" command returned an empty result.'.format(command))

    @log_method
    def get_databases_names(self):
        is_failed = True
        databases = []
        command = "JSON.stringify(db.adminCommand({ listDatabases: 1}))"
        try:
            json_result = json.loads(self.eval(command, True))
        except Exception as e:
            try:
                try:
                    json_result = json.loads(self.eval("rs.slaveOk();" + command), True)
                except:
                    try:
                        json_result = json.loads(self.eval("rs.secondaryOk();" + command), True)
                    except:
                        raise e

            finally:
                e = None
                del e

        else:
            if "ok" in json_result:
                if json_result["ok"] != 1:
                    raise Exception(json_result)
            if "databases" in json_result:
                is_failed = False
                for d in json_result["databases"]:
                    if "name" in d:
                        databases.append(d["name"])

            elif is_failed:
                raise Exception("Failed to get dabatabases list")
            return databases

    @log_method
    def test_db_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def handle_scripts(self, script, timeout):
        joined_script = "".join(script)
        params = self.helper.get_params_to_run_server_script(self.get_mongo_cli_path(), ' --quiet --eval "{0}"'.format(joined_script), self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "make_tcp_request_to_mongo", params=(params,), attempts=1, time_out=timeout)

    @log_method
    def get_name_and_type_for_backup(self, db_name, backup_type, backup_name):
        backup_data = {
         'backup_type': backup_type, 
         'backup_name': backup_name, 
         'raise_type': None, 
         'raise_data': None}
        return backup_data

    @log_method
    def get_current_backup_type(self, db_name, backup_type):
        return backup_type

    @log_method
    def get_non_system_databases(self):
        return [d for d in self.get_databases_names() if d not in SYSTEM_DATABASES_MONGO]

    @log_method
    def get_connection_settings_as_xml(self, dbms_connection):
        return "<MongoDbConnectionInfo Host='{0}' Port='{1}' User='{2}' Password='{3}' AuthDatabaseName='{4}' />".format(self.helper.check_none(dbms_connection["Host"]), self.helper.check_none(dbms_connection["Port"]), self.helper.check_none(dbms_connection["User"]), self.helper.check_none(dbms_connection["Password"]), self.get_auth_database(dbms_connection["Database"]))
