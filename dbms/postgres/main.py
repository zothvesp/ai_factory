
import json
from sqlbak.helpers.temporary_directory import create_directory, create_temp_dir, remove_temp_resource
from sqlbak.definitions import SYSTEM_DATABASES_POSTGRESQL, SQL_SCRIPT_TYPE
from sqlbak.helper import Helper
from sqlbak.logger import log_data, log_method
from sqlbak.native_command import NativeCommand
from sqlbak.job_log import JobLog

class PostgreSql:

    @log_method
    def __init__(self, params=None):
        self.helper = Helper()
        self.job_log = JobLog()
        self.params = params
        self.utils = json.loads(self.params["UtilsPath"])
        self.native_command = NativeCommand()

    @log_method
    def get_optional_params(self, command, request):
        params = self.helper.get_params_to_run_server_script(command, request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        allowed_params = self.native_command.get_allowed_psql_params(params)
        optional_params = []
        for p in self.params["PS_PARAMS"]:
            if p != "--lock-wait-timeout" and p != "--format" and self.is_param_allowed(p, self.params["PS_PARAMS"][p], allowed_params):
                optional_params.append(p)
            optional_params = self.add_lock_time_param(allowed_params, optional_params)
            optional_params = self.add_format_param(allowed_params, optional_params)
            optional_params = self.add_custom_params(allowed_params, optional_params)
            return optional_params

    @log_method
    def add_format_param(self, allowed_params, optional_params):
        if self.is_param_allowed("--format", True, allowed_params):
            optional_params.append("--format={0}".format(self.params["PS_PARAMS"]["--format"]))
        return optional_params

    @log_method
    def add_lock_time_param(self, allowed_params, optional_params):
        if self.is_param_allowed("--lock-wait-timeout", True, allowed_params):
            optional_params.append("--lock-wait-timeout={0}".format(self.params["PS_PARAMS"]["--lock-wait-timeout"]))
        return optional_params

    @log_method
    def add_custom_params(self, allowed_params, optional_params):
        if "PS_PARAMS" in self.params:
            if "--custom-arguments" in self.params["PS_PARAMS"]:
                if self.params["PS_PARAMS"]["--custom-arguments"]:
                    for p in self.params["PS_PARAMS"]["--custom-arguments"].split():
                        if p.startswith("--"):
                            arg = p.split("=")[0]
                        else:
                            arg = ""
                        if arg in optional_params:
                            raise Exception("Cannot override argument: '{0}'".format(p))
                        else:
                            optional_params.append(p)

        return optional_params

    @log_method
    def is_param_allowed(self, param, param_value, allowed_params):
        is_allowed = False
        should_check_params = len(allowed_params) > 0
        if should_check_params:
            if param in allowed_params and param_value:
                is_allowed = True
        else:
            is_allowed = True
        return is_allowed

    @log_method
    def make_tcp_request(self, command, request=''):
        """

        :param command:
        :param request:
        :return:
        """
        params = self.helper.get_params_to_run_server_script(command, request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return self.native_command.make_tcp_request_to_postgresql(params)

    @log_method
    def get_databases_names(self):
        command = "-t -A -d {0} -c 'SELECT datname FROM pg_database'".format(self.get_auth_database())
        result = self.make_tcp_request(self.utils["psql-path"], command)
        if result:
            return result.split("\n")
        return []

    @log_method
    def get_non_system_databases(self):
        return [database for database in self.get_databases_names() if database not in SYSTEM_DATABASES_POSTGRESQL]

    @log_method
    def test_db_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def handle_scripts(self, script, timeout):
        """

        :param script:
        :param timeout:
        :return:
        """
        script_folder = create_temp_dir(None, "script")
        script_file = script_folder + "script.sql"
        scipt_chunks = [
         {'db':(self.get_auth_database)(), 
          'lines':[]}]
        for line in script:
            if line:
                if line.startswith("--@psql /c"):
                    scipt_chunks += [{'db':(line.replace("--@psql /c", "").strip(";").strip)(" "),  'lines':[]}]
                else:
                    scipt_chunks[-1]["lines"] += [line]
            result = ""
            for script in [x for x in scipt_chunks if len(x["lines"]) > 0]:
                try:
                    with open(script_file, "w") as f:
                        for line in script["lines"]:
                            f.write(line + "\n")

                    params = self.helper.get_params_to_run_server_script(self.utils["psql-path"], '-t -A -d {0} -v "ON_ERROR_STOP=1" < \'{1}\' '.format(script["db"], script_file), self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
                    result += "\n" + str(self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "make_tcp_request_to_postgresql", params=(
                     params,),
                      attempts=1,
                      time_out=timeout))
                finally:
                    remove_temp_resource(script_file)

            else:
                return result

    @log_method
    def get_current_backup_type(self, db_name, backup_type):
        return backup_type

    @log_method
    def get_name_and_type_for_backup(self, db_name, backup_type, backup_name):
        return {
         'backup_type': backup_type, 
         'backup_name': backup_name, 
         'raise_type': None, 
         'raise_data': None}

    @log_method
    def get_connection_settings_as_xml(self, dbms_connection):
        return "<PostgreSqlConnectionInfo Server='{0}' Port='{1}' Login='{2}' Password='{3}' SslMode='Prefer' PasswordSetterType='Environment' />".format(self.helper.check_none(dbms_connection["Host"]), self.helper.check_none(dbms_connection["Port"]), self.helper.check_none(dbms_connection["User"]), self.helper.check_none(dbms_connection["Password"]))

    @log_method
    def get_auth_database(self, database=None):
        if database is None:
            if "Database" in self.params:
                if self.params["Database"] is not None:
                    database = self.params["Database"]
        auth_database = "postgres"
        if database is not None:
            auth_database = database.strip()
        return auth_database
