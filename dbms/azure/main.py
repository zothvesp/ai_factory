import os, json, time
from sqlbak.definitions import CONFIG, BACKUP_TYPES, FULL_BACKUP_CONST, SQL_SCRIPT_TYPE, CONSOLE_COLORS, SYSTEM_DATABASES_MSSQL
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_method
from sqlbak.app_output import APP_OUTPUT

class AzureMain:

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
    def make_tcp_request(self, request=''):
        params = self.helper.get_params_to_run_server_script(self.utils["sqlcmd-path"], request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return self.native_command.make_tcp_request_to_mssql(params)

    @log_method
    def make_sqlpackage_request_export(self, request=''):
        return self.native_command.make_tcp_request_to_sqlpackage_export((
         self.params["Host"],
         self.params["User"],
         self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None,
         self.utils["sqlpackage-path"],
         request))

    @log_method
    def make_sqlpackage_request_import(self, request=''):
        return self.native_command.make_tcp_request_to_sqlpackage_import((
         self.params["Host"],
         self.params["User"],
         self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None,
         self.utils["sqlpackage-path"],
         request))

    @log_method
    def get_databases_names(self):
        result = self.make_tcp_request("-Q 'SELECT name FROM master.sys.databases;'")
        db_list = []
        if result:
            for d in result.split("\n")[2[:-3]]:
                db_list.append(d.strip())

        return db_list

    @log_method
    def test_db_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def handle_scripts(self, script, timeout):
        """

        :param script:
        :param timeout:
        :return:
        """
        params = self.helper.get_params_to_run_server_script(self.utils["sqlcmd-path"], '-Q "{0};"'.format("".join(script)), self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        res = self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "make_tcp_request_to_mssql", params=(params,), attempts=1, time_out=timeout)
        if "State" in res:
            raise Exception(self.cm["FAILED_VERIFY_AFTER_BACKUP"].format(res))
        return res

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
        return [d for d in self.get_databases_names() if d not in SYSTEM_DATABASES_MSSQL]

    @log_method
    def get_connection_settings_as_xml(self, dbms_connection):
        return "<AzureDbConnectionInfo Server='{0}' UserName='{1}' Password='{2}' />".format(self.helper.check_none(dbms_connection["Host"]), self.helper.check_none(dbms_connection["User"]), self.helper.check_none(dbms_connection["Password"]))

    @log_method
    def get_azure_configurationParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def create_azure_database(self, target_database_name, asCopy, azure_configuration):
        query = "CREATE DATABASE [{}] ".format(target_database_name)
        if asCopy:
            query += "AS COPY OF [{}] ".format(asCopy)
        elif azure_configuration != None:
            if azure_configuration["ElasticPoolName"].lower() == "null":
                query += "(EDITION='{azure_configuration[Edition]}', SERVICE_OBJECTIVE='{azure_configuration[ServiceObjective]}')".format(azure_configuration=azure_configuration)
            else:
                query += "(name={azure_configuration[ElasticPoolName]})".format(azure_configuration=azure_configuration)
        error_message = self.make_tcp_request('-Q "{}"'.format(query))
        if error_message:
            raise Exception(error_message)

    @log_method
    def rename_database(self, source_database_name, target_database_name):
        query = "ALTER DATABASE [{}] MODIFY NAME=[{}]".format(source_database_name, target_database_name)
        self.make_tcp_request('-Q "{}"'.format(query))

    @log_method
    def drop_database(self, database_name):
        query = "DROP DATABASE [{}]".format(database_name)
        self.make_tcp_request("-Q '{}'".format(query))

    @log_method
    def export_attemptsParse error at or near `COLLECTION_START' instruction at offset 0_0
