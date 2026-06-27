
import os, json, sqlbak.helpers.strings
from sqlbak.definitions import SYSTEM_DATABASES_MYSQL, CONFIG, MYSQL_CONST, BACKUP_TYPES, INC_BACKUP_CONST, FULL_BACKUP_CONST, MYSQL_DATA_SCHEMA_HAS_CHANGED, BACKUP_TYPE_CHANGED, MYSQL_DUMP_CHECKSUM_PARAMS, SQL_SCRIPT_TYPE, MYSQL_BIN_LOG_PARAMS_ON_GALERA, MYSQL_BIN_LOG_PARAMS, CONSOLE_COLORS, INC_BACKUP_SUFFIX, DOCKER_EXEC, SUDO_SQLBAK
from sqlbak.helper import Helper
from sqlbak.job_log import JobLog
from sqlbak.local_db import LocalDB
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_data, log_method
from sqlbak.app_output import APP_OUTPUT
from sqlbak.dbms.mysql.inc_helper import get_last_binlog

class MySql:

    @log_method
    def __init__(self, params=None):
        self.helper = Helper()
        self.params = params
        self.utils = json.loads(self.params["UtilsPath"])
        self.job_log = JobLog()
        self.local_db = LocalDB()
        self.native_command = NativeCommand()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def get_params_for_request(self, command, request=''):
        params = self.helper.get_params_to_run_server_script(command, request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return params

    @log_method
    def make_tcp_request(self, command, request=''):
        """

        :param command:
        :param request:
        :return:
        """
        params = self.get_params_for_request(command, request)
        password_in_env = self.params["My_PasswordInEnv"] if "My_PasswordInEnv" in self.params else False
        return self.native_command.make_tcp_request_to_mysql(params, password_in_env)

    @log_method
    def get_databases_names(self):
        result = self.make_tcp_request(self.utils["mysql-path"], '-e "show databases;"')
        if result:
            return [d for d in result.split("\n") if d != "Database"]
        return []

    def get_creation_time_for_all_databases(self):
        result = self.make_tcp_request(self.utils["mysql-path"], '-e "SELECT SCHEMA_NAME, CREATE_TIME FROM INFORMATION_SCHEMA.SCHEMATA;"')
        if result:
            print([d for d in result.split("\n") if d != "Database"])
            return [d for d in result.split("\n") if d != "Database"]
        return []

    @log_method
    def get_non_system_databases(self):
        return [database for database in self.get_databases_names() if database not in SYSTEM_DATABASES_MYSQL]

    @log_method
    def test_db_connectionParse error at or near `LOAD_CONST' instruction at offset 0

    @log_method
    def handle_scripts(self, script, timeout):
        """

        :param script:
        :param timeout:
        :return:
        """
        script = [sqlbak.helpers.strings.escape_backticks(x) for x in script if x]
        variables = ""
        if "CountJobErrors" in self.params:
            job_success_variable = 0 if self.params["CountJobErrors"] > 0 else 1
            variables += "SET @SQLBAK_JOB_SUCCESS = {0};".format(job_success_variable)
        if "BackupType" in self.params:
            backup_type_varriable = self.params["BackupType"]
            variables += "SET @SQLBAK_BACKUP_TYPE = '{0}';".format(backup_type_varriable)
        if "ObjectName" in self.params:
            variables += "SET @SQLBAK_DATABASE_NAME = '{0}';".format(self.params["ObjectName"])
        joined_script = variables + "".join(script)
        params = self.helper.get_params_to_run_server_script(self.utils["mysql-path"], '-e "{0};"'.format(joined_script), self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        password_in_env = self.params["My_PasswordInEnv"] if "My_PasswordInEnv" in self.params else False
        return self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "make_tcp_request_to_mysql", params=(params, password_in_env), attempts=1, time_out=timeout)

    @log_method
    def get_optional_parameters(self):
        optional_parameters = []
        if self.params["My_SqlUseTransaction"]:
            optional_parameters.append("--single-transaction")
        elif self.params["My_LockTables"]:
            optional_parameters.append("--lock-tables")
        if self.params["My_SQLCompatibility"]:
            optional_parameters.append("--compatible={0}".format(self.params["My_SQLCompatibility"]))
        if self.params["My_SqlColumnStatistics"] is not None:
            if self.params["My_SqlColumnStatistics"]:
                optional_parameters.append("--column-statistics=1")
            else:
                optional_parameters.append("--column-statistics=0")
        if self.params["My_SQLIncludeComments"]:
            optional_parameters.append("--comments")
        if self.params["My_SqlDropTable"]:
            optional_parameters.append("--add-drop-table")
        if self.params["My_SqlBackQuotes"]:
            optional_parameters.append("--quote-names")
        if self.params["My_SqlProcedureFunction"]:
            optional_parameters.append("--routines")
        if self.params["My_Events"]:
            optional_parameters.append("--events")
        if self.params["My_NoCreateDatabaseStatement"]:
            optional_parameters.append("--no-create-db")
        if self.params["My_SqlColumns"]:
            optional_parameters.append("--complete-insert")
        if self.params["My_SqlExtended"]:
            optional_parameters.append("--extended-insert")
        optional_parameters.append("--max-allowed-packet={0}M".format(self.params["My_MaxAllowedPacket"]))
        if self.params["My_SqlIgnore"]:
            optional_parameters.append("--insert-ignore")
        if self.params["My_SqlHexForBlob"]:
            optional_parameters.append("--hex-blob")
        if self.params["My_SqlType"]:
            optional_parameters.append("--replace")
        if self.params["My_SqlData"]:
            if not self.params["My_SqlStructure"]:
                optional_parameters.append("--no-create-info")
        if not self.params["My_SqlData"]:
            if self.params["My_SqlStructure"]:
                optional_parameters.append("--no-data")
        if self.params["My_ExtraCommandLineParameters"]:
            optional_parameters.append(self.params["My_ExtraCommandLineParameters"])
        return optional_parameters

    mysql_dump_parameters = None

    @log_method
    def mysqldump_is_support_parameter(self, parameter_name):
        self.mysql_dump_parameters = self.make_tcp_request(self.utils["mysqldump-path"], "--help") if self.mysql_dump_parameters is None else self.mysql_dump_parameters
        return parameter_name in self.mysql_dump_parameters

    mysqlbinlog_parameters = None

    @log_method
    def mysqlbinlog_is_support_parameter(self, parameter_name):
        self.mysqlbinlog_parameters = self.make_tcp_request("mysqlbinlog", "--help") if self.mysqlbinlog_parameters is None else self.mysqlbinlog_parameters
        return parameter_name in self.mysqlbinlog_parameters

    def get_variable_value(self, variable_name):
        res = self.make_tcp_request(self.utils["mysql-path"], '--silent --batch -e "SHOW VARIABLES LIKE \'{0}\'"'.format(variable_name))
        if res:
            return res.split("\t")[1].strip()
        return

    @log_method
    def is_bin_log_enabled(self):
        log_bin_val = self.get_variable_value("log_bin").lower()
        if log_bin_val:
            return log_bin_val.lower() == "on"
        return False

    def is_galera(self):
        wsrep_on_val = self.mysqldump_is_support_parameter("wsrep_on")
        if wsrep_on_val:
            return wsrep_on_val.lower() == "on"
        return False

    @log_method
    def is_row_format_enabled(self):
        binlog_format_val = self.get_variable_value("binlog_format").lower()
        if binlog_format_val:
            return binlog_format_val.lower() == "row"
        return False

    @log_method
    def get_server_id(self):
        return self.get_variable_value("server_id")

    @log_method
    def save_current_backup_index(self, job_id):
        binlog_index_path = self.get_path_to_log_bin_index()
        binlog = get_last_binlog(binlog_index_path)
        self.local_db.save_backuped_binlog(binlog_index_path, job_id, binlog)

    @log_method
    def get_path_to_log_bin_index(self):
        if sqlbak.helpers.strings.is_not_empty(self.utils["mysql-binlog-index-path"]):
            return self.utils["mysql-binlog-index-path"]
        return self.get_variable_value("log_bin_index")

    @log_method
    def get_path_to_logs_lib(self):
        if sqlbak.helpers.strings.is_not_empty(self.utils["mysql-binlog-base-path"]):
            return self.utils["mysql-binlog-base-path"]
        res = self.make_tcp_request(self.utils["mysql-path"], '-e "SHOW VARIABLES LIKE \'log_bin_basename\'"')
        split_result = res.split("\n")
        if len(split_result) > 1:
            variables = split_result[1].split()
            return "/".join(variables[1].split("/")[0[:-1]]) + "/"
        return

    @log_method
    def get_current_backup_type(self, db_name, backup_type):
        if backup_type == INC_BACKUP_CONST:
            last_backup_type = self.local_db.get_last_backup_type_for_job_id(self.params["JobId"])
            backup_type = backup_type if (last_backup_type is not None and self.helper.check_if_previous_backup_was_success(db_name, last_backup_type, self.local_db, self.params["JobId"])) else FULL_BACKUP_CONST
        return backup_type

    @log_method
    def get_name_and_type_for_backup(self, db_name, backup_type, backup_name):
        backup_data = {'backup_type':backup_type, 
         'backup_name':backup_name, 
         'raise_type':None, 
         'raise_data':{'DatabaseName':db_name, 
          'CurrentBackupType':backup_type}}
        if backup_type == INC_BACKUP_CONST:
            self.check_allow_binlog()
            backup_data["backup_name"] = str(self.params["ConnectionName"]) + str(self.params["BackupAt"].strftime("%Y%m%d%H%M")) + INC_BACKUP_SUFFIX
            res = self.does_dump_checksum_changed(db_name, self.params["JobId"])
            if res["HasChanged"]:
                if res["CurrentChecksum"] is not None:
                    if res["CurrentChecksum"] != res["PreviousChecksum"]:
                        self.local_db.save_checksum_for_dump_file(res["CurrentChecksum"], db_name, self.params["JobId"])
            else:
                backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], FULL_BACKUP_CONST)
                backup_data.update({'backup_type':FULL_BACKUP_CONST, 
                 'backup_name':backup_name, 
                 'raise_type':MYSQL_DATA_SCHEMA_HAS_CHANGED})
                return backup_data
                if not self.local_db.get_last_backuped_binlog(self.get_path_to_log_bin_index(), self.params["JobId"]):
                    backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], FULL_BACKUP_CONST)
                    backup_data.update({'backup_type':FULL_BACKUP_CONST, 
                     'backup_name':backup_name, 
                     'raise_type':BACKUP_TYPE_CHANGED, 
                     'raise_data':{'DatabaseName':db_name, 
                      'CurrentBackupType':backup_type, 
                      'Reason':self.cm["NO_INFO_PREVIOS_BACKUP"]}})
                    return backup_data
                global_last_backup_object = self.local_db.get_last_backup_object(self.params["JobId"])
                last_backup_object = self.local_db.get_last_backup_object(self.params["JobId"], db_name)
                if global_last_backup_object is None or last_backup_object is None or global_last_backup_object["BackupId"] != last_backup_object["BackupId"]:
                    backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], FULL_BACKUP_CONST)
                    backup_data.update({'backup_type':FULL_BACKUP_CONST, 
                     'backup_name':backup_name, 
                     'raise_type':BACKUP_TYPE_CHANGED, 
                     'raise_data':{'DatabaseName':db_name, 
                      'CurrentBackupType':backup_type, 
                      'Reason':self.cm["NO_INFO_PREVIOS_BINLOG"]}})
            if not int(last_backup_object["IsSuccess"]):
                backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], FULL_BACKUP_CONST)
                backup_data.update({'backup_type':FULL_BACKUP_CONST, 
                 'backup_name':backup_name, 
                 'raise_type':BACKUP_TYPE_CHANGED, 
                 'raise_data':{'DatabaseName':db_name, 
                  'CurrentBackupType':backup_type, 
                  'Reason':self.cm["PREVIOS_BACKUP_FAILED"]}})
        return backup_data

    @log_method
    def calculate_and_return_checksum_for_file(self, db_name, job_id):
        working_dir = self.local_db.get_working_dir()
        path_to_test_dump_file = working_dir + "dump_{0}_{1}.sql".format(db_name, str(job_id))
        self.make_test_dbms_dump(db_name, path_to_test_dump_file)
        dump_checksum = self.helper.get_checksum_for_file(path_to_test_dump_file)
        self.helper.remove_file_or_dir([path_to_test_dump_file])
        return dump_checksum

    @log_method
    def does_dump_checksum_changed(self, db_name, job_id):
        is_checksum_changed = False
        dump_checksum = self.calculate_and_return_checksum_for_file(db_name, job_id)
        previous_dump_checksum = self.local_db.get_checksum_for_dump_file(db_name, job_id)
        if dump_checksum is None or previous_dump_checksum is None or dump_checksum != previous_dump_checksum:
            is_checksum_changed = True
        return {'HasChanged':is_checksum_changed,  'CurrentChecksum':dump_checksum,  'PreviousChecksum':previous_dump_checksum}

    @log_method
    def make_test_dbms_dump(self, db_name, path_to_database_backup):
        optional_params = []
        if self.params["My_SqlColumnStatistics"] is not None:
            if self.params["My_SqlColumnStatistics"]:
                optional_params.append("--column-statistics=1")
            else:
                optional_params.append("--column-statistics=0")
        self.make_tcp_request(self.utils["mysqldump-path"], ' --databases "{1}" {0} {3} > "{2}" '.format(" ".join(MYSQL_DUMP_CHECKSUM_PARAMS), db_name, path_to_database_backup, " ".join(optional_params)))
        self.native_command.remove_auto_increment_from_dump(path_to_database_backup)

    @log_method
    def check_if_mysql_schema_has_changed(self, database_data, job_id, path_to_backup, file_format, backup_at):
        is_schema_changed = False
        backup_name = database_data["BackupName"]
        backup_type = database_data["CurrentBackupType"]
        res = self.does_dump_checksum_changed(database_data["DatabaseName"], job_id)
        if res["HasChanged"]:
            is_schema_changed = True
            if res["CurrentChecksum"] is not None:
                if res["CurrentChecksum"] != res["PreviousChecksum"]:
                    self.local_db.save_checksum_for_dump_file(res["CurrentChecksum"], database_data["DatabaseName"], job_id)
            self.helper.remove_file_or_dir([path_to_backup + backup_name + database_data["BackupExtension"]])
            backup_type = FULL_BACKUP_CONST
            backup_name = self.helper.get_backup_file_name(file_format, database_data["DatabaseName"], backup_at, FULL_BACKUP_CONST)
        return {'backup_name':backup_name,  'backup_type':backup_type,  'is_schema_changed':is_schema_changed}

    @log_method
    def make_copy_bin_log_settings(self, path_to_file):
        if os.path.exists(path_to_file):
            if not os.path.exists("/etc/mysql/my.cnf.old"):
                native_command = NativeCommand()
                native_command.copy_resource(path_to_file, "/etc/mysql/my.cnf.old")
        if not os.path.exists(path_to_file):
            with open(path_to_file, "a+") as f:
                pass

    @log_method
    def handle_user_enter(self, txt):
        if txt.strip().lower() != "y":
            return
        path_to_file = "/etc/mysql/my.cnf"
        self.make_copy_bin_log_settings(path_to_file)
        content = []
        is_mysqld_present = False
        binlogs_param = MYSQL_BIN_LOG_PARAMS_ON_GALERA if not self.is_galera() else MYSQL_BIN_LOG_PARAMS
        with open(path_to_file, "r") as f:
            checked_params = [p for p in binlogs_param]
            checked_params.insert(0, "[mysqld]")
            for line in f.readlines():
                strip_line = line.strip()
                if strip_line:
                    if strip_line not in content:
                        content.append(strip_line)
                    if "[mysqld]" in strip_line:
                        if "[mysqld]" in checked_params:
                            checked_params.remove("[mysqld]")
                        is_mysqld_present = True
                    if is_mysqld_present:
                        checked_params = self.handle_bin_log_params(content, strip_line, checked_params)
            else:
                if len(checked_params) > 0:
                    for p in checked_params:
                        if p not in binlogs_param:
                            content.append(str(p))
                        else:
                            content.append(str(p) + " = " + str(binlogs_param[p]))

        self.update_settings_file(path_to_file, content)
        self.restart_mysql_server()

    @log_method
    def update_settings_file(self, path_to_file, content):
        if len(content) > 0:
            with open(path_to_file, "w") as f:
                f.write("\n".join(content))

    @log_method
    def handle_bin_log_params(self, content, strip_line, checked_params):
        for p in MYSQL_BIN_LOG_PARAMS:
            if p in strip_line:
                split_line = strip_line.split("=")
                value = split_line[1].strip()
                l = str(p) + " = " + str(MYSQL_BIN_LOG_PARAMS[p])
                if str(value) == str(MYSQL_BIN_LOG_PARAMS[p]):
                    if strip_line[0] == "#" and l not in content:
                        content.append(l)
                elif strip_line[0] != "#":
                    if "#" + strip_line not in content:
                        content.append("#" + strip_line)
                if l not in content:
                    content.append(l)
                if p in checked_params:
                    checked_params.remove(p)
            return checked_params

    @log_method
    def restart_mysql_server(self):
        res = self.native_command.restart_mysql_service()
        if res is not None:
            if int(res) == 0:
                if self.is_bin_log_enabled() and self.is_row_format_enabled():
                    self.helper.print_color_text(self.cm["CORRECT_BIN_LOG_SETTINGS"], CONSOLE_COLORS["GREEN"])
            else:
                self.helper.print_color_text(self.cm["FAILED_RESTART_MYSQL"], CONSOLE_COLORS["GREEN"])

    @log_method
    def get_connection_settings_as_xml(self, dbms_connection):
        return "<MySqlConnectionInfo SqlServerHost='{0}' MySqlPort='{1}' UserName='{2}' Password='{3}' UseSsh='{4}' SshHostname='{5}' SshPort='{6}' SshMappedPort='{7}' SshUserName='{8}' SshPassword='{9}' Timeout='30' />".format(self.helper.check_none(dbms_connection["Host"]), self.helper.check_none(dbms_connection["Port"]), "root" if (dbms_connection["User"] is None or dbms_connection["User"] == "") else (dbms_connection["User"]), str(self.helper.check_none(dbms_connection["Password"])), bool(dbms_connection["UseSsh"]), self.helper.check_none(dbms_connection["SshHost"]), self.helper.check_none(dbms_connection["SshPort"]), self.helper.check_none(dbms_connection["SshLocalMappedPort"]), self.helper.check_none(dbms_connection["SshUser"]), str(self.helper.check_none(dbms_connection["SshPassword"])))

    def check_allow_binlog(self):
        if not self.is_bin_log_enabled():
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            raise Exception(self.cm["BIN_LOG_DISABLED"].format(self.params["ConnectionId"], msg_param))

    def is_maria_db(self):
        full_help = self.make_tcp_request(self.utils["mysql-path"], "--help")
        return "maria" in full_help.lower()
