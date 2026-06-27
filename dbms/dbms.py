from datetime import datetime
from sqlbak.definitions import DBMS_TYPES_CONSTS, RUN_SCRIPT_TYPES, AVAILABLE_SERVER_TYPES, CONFIG, FULL_BACKUP_CONST, LOG_BACKUP_CONST, DIFF_BACKUP_CONST, INC_BACKUP_CONST, PREVIOUS_BACKUP_HAS_FAILED, BACKUP_TYPES, FULL_AND_FIRST_BACKUP, MYSQL_CONST, MSSQL_CONST, POSTGRESQL_CONST, MARIADB_CONST, POSTGRES_CONST, XTRABACKUP_CONST, MONGO_CONST, MONGODB_CONST, AZURESQL_CONST
from sqlbak.logger import log_method
from sqlbak.job_log import JobLog
from sqlbak.dbms.mssql.main import MsSqlServer
from sqlbak.dbms.mysql.main import MySql
from sqlbak.dbms.postgres.main import PostgreSql
from sqlbak.native_command import NativeCommand
from sqlbak.helper import Helper
from sqlbak.exchange_message.remote_server_requests import RemoteServerRequest
from sqlbak.local_db import LocalDB
from sqlbak.dbms.mysql.inc import MySqlInc
from sqlbak.dbms.mysql.full import MySqlFull
from sqlbak.dbms.postgres.full import PostgreSqlFull
from sqlbak.dbms.mssql.full import MsSqlServerFull
from sqlbak.dbms.mssql.diff import MsSqlServerDiff
from sqlbak.dbms.mssql.log import MsSqlServerLog
from sqlbak.dbms.xtrabackup.full import XtrabackupFull
from sqlbak.dbms.xtrabackup.inc import XtrabackupInc
from sqlbak.dbms.mongodb.main import MongoMain
from sqlbak.dbms.mongodb.full import MongoDbFull
from sqlbak.dbms.azure.main import AzureMain
from sqlbak.dbms.azure.full import AzureFull
from sqlbak.app_output import APP_OUTPUT

class DBMS:

    def __init__(self, params=None):
        self.helper = Helper()
        self.params = params
        self.native_command = NativeCommand()
        self.local_db = LocalDB()
        self.remote_request = RemoteServerRequest()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def get_db_server_class_instance(self, backup_type=None):
        """
        A method to get a SQL server database class instance
        :return:
        """
        db_class = self.get_db_class(backup_type)
        db_instance = db_class(self.params)
        return db_instance

    @log_method
    def get_db_class(self, backup_type):
        """
        A method to get a db class according to a server type
        :return: db class
        """
        if self.params["ServerType"] not in DBMS_TYPES_CONSTS:
            raise Exception(self.cm["WRONG_SERVER_TYPE"].format(self.params["ServerType"], ", ".join(AVAILABLE_SERVER_TYPES)))
        database_server_list = {MYSQL_CONST: {"main": MySql, 
                       FULL_BACKUP_CONST: MySqlFull, 
                       INC_BACKUP_CONST: MySqlInc}, 
         
         POSTGRESQL_CONST: {"main": PostgreSql, 
                            FULL_BACKUP_CONST: PostgreSqlFull}, 
         
         MSSQL_CONST: {"main": MsSqlServer, 
                       FULL_BACKUP_CONST: MsSqlServerFull, 
                       LOG_BACKUP_CONST: MsSqlServerLog, 
                       DIFF_BACKUP_CONST: MsSqlServerDiff}, 
         
         MARIADB_CONST: {"main": MySql, 
                         FULL_BACKUP_CONST: MySqlFull, 
                         INC_BACKUP_CONST: MySqlInc}, 
         
         POSTGRES_CONST: {"main": PostgreSql, 
                          FULL_BACKUP_CONST: PostgreSqlFull}, 
         
         XTRABACKUP_CONST: {"main": MySql, 
                            FULL_BACKUP_CONST: XtrabackupFull, 
                            INC_BACKUP_CONST: XtrabackupInc}, 
         
         MONGO_CONST: {"main": MongoMain, 
                       FULL_BACKUP_CONST: MongoDbFull}, 
         
         MONGODB_CONST: {"main": MongoMain, 
                         FULL_BACKUP_CONST: MongoDbFull}, 
         
         AZURESQL_CONST: {"main": AzureMain, 
                          FULL_BACKUP_CONST: AzureFull}}
        return database_server_list[self.params["ServerType"]][backup_type if backup_type else "main"]

    @log_method
    def get_databases_names(self):
        db_instance = self.get_db_server_class_instance()
        databases = db_instance.get_databases_names()
        return databases

    @log_method
    def get_non_system_databases(self):
        db_instance = self.get_db_server_class_instance()
        return db_instance.get_non_system_databases()

    @log_method
    def test_db_connection(self):
        """
        A method to test a SQL database connection
        :return:
        """
        db_instance = self.get_db_server_class_instance()
        connection_result = db_instance.test_db_connection()
        return {'is_success':connection_result["connection"],  'error':connection_result["connection_error"]}

    @log_method
    def run_scripts_before_backup(self):
        for s in self.params["JobScripts"]:
            if s["IsBeforeBackup"]:
                self.handle_scripts(s["Script"], s["Timeout"], RUN_SCRIPT_TYPES["BEFORE_BACKUP"], s["IsSqlScript"])

    @log_method
    def run_scripts_after_backup(self):
        for s in self.params["JobScripts"]:
            if not s["IsBeforeBackup"]:
                self.handle_scripts(s["Script"], s["Timeout"], RUN_SCRIPT_TYPES["AFTER_BACKUP"], s["IsSqlScript"])

    @log_method
    def backup(self, database_data, path_to_backup):
        """

        :param db_name:
        :param path_to_backup:
        :param backup_name:
        :return:
        """
        db_instance = self.get_db_server_class_instance(database_data["CurrentBackupType"] if database_data["CurrentBackupType"] is not None else self.params["BackupType"])
        db_instance.backup_database(database_data, path_to_backup)

    @log_method
    def handle_scripts(self, script, timeout, script_type, is_script=True):
        """

        :param script:
        :param timeout:
        :param script_type:
        :param is_script:
        :return:
        """
        job_log = JobLog()
        msg = "SQL" if is_script else "cmd"
        self.add_backup_script_record_to_log(job_log, script_type, msg)
        self.run_backup_script(job_log, script, timeout, is_script, msg)

    @log_method
    def add_backup_script_record_to_log(self, job_log, script_type, msg):
        """

        :param job_log:
        :param script_type:
        :param msg:
        :return:
        """
        if script_type == RUN_SCRIPT_TYPES["BEFORE_BACKUP"]:
            self.params = job_log.run_script_before_backup(self.params, msg)
        else:
            if script_type == RUN_SCRIPT_TYPES["AFTER_BACKUP"]:
                self.params = job_log.run_script_after_backup(self.params, msg)
            else:
                if script_type == RUN_SCRIPT_TYPES["MAINTENANCE"]:
                    self.params = job_log.run_maintenance_job_script(self.params, msg)

    @log_method
    def run_backup_script(self, job_log, script, timeout, is_script, msg):
        """

        :param job_log:
        :param script:
        :param timeout:
        :param is_script:
        :param msg:
        :return:
        """
        try:
            if is_script:
                db_instance = self.get_db_server_class_instance()
                res = db_instance.handle_scripts(script, timeout)
                self.params = job_log.run_job_sql_script_output(self.params, res)
            else:
                if "CountJobErrors" in self.params:
                    if "BackupType" in self.params:
                        job_success_variable = 0 if self.params["CountJobErrors"] > 0 else 1
                        backup_type_varriable = self.params["BackupType"]
                        script = ["SQLBAK_JOB_SUCCESS={0}\n".format(job_success_variable)] + script
                        script = ["SQLBAK_BACKUP_TYPE='{0}'\n".format(backup_type_varriable)] + script
                res = self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "run_linux_script_as_file", params=(script,), attempts=1, time_out=timeout)
                self.params = job_log.run_job_bash_script_output(self.params, res)
        except Exception as e:
            try:
                raise Exception("Failed to run a job script. {0}".format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def restore_backup(self, restore_data):
        db_instance = self.get_db_server_class_instance(self.params["BackupType"])
        return db_instance.restore(restore_data)

    @log_method
    def check_dbms_connections(self):
        agent = self.local_db.get_current_agent()
        if agent is None:
            return
        dbms_connection_states = self.get_dbms_connection_states(agent)
        if len(dbms_connection_states) > 0:
            res = self.remote_request.notify_about_dbms_connection(agent["AgentKey"], dbms_connection_states)
            if not res["IsSuccess"]:
                raise Exception(self.cm["FAILED_TEST_CONNECTION_STATE"].format(str(res["ErrorMessage"])))

    @log_method
    def get_dbms_connection_states(self, agent):
        dbms_connection_states = []
        for connection in self.local_db.get_dbms_connections():
            dbms_connection_state = self.check_dbms_connection_state(agent, connection)
            if dbms_connection_state is not None:
                dbms_connection_states.append(dbms_connection_state)
            return dbms_connection_states

    @log_method
    def check_dbms_connection_state(self, agent, connection):
        self.get_connection_params(agent, connection)
        test_connection_result = self.test_db_connection()
        return self.check_dbms_connection(test_connection_result)

    @log_method
    def get_connection_params(self, agent, connection):
        self.params = {'UtilsPath':agent["UtilsPath"], 
         'AgentName':agent["AgentName"]}
        self.params.update(connection)

    @log_method
    def check_dbms_connection(self, test_connection_result):
        check_result = None
        is_success = int(not test_connection_result["is_success"])
        connection_state = self.local_db.get_dbms_connection_state(self.params["ConnectionId"])
        if connection_state is None or int(connection_state["State"]) != is_success:
            date_time = datetime.now()
            connection_state = self.get_connection_state_from_local_db(connection_state, is_success, date_time)
            dbms_type = self.helper.get_dbms_type_by_name(connection_state["ServerType"], connection_state["ConnectionType"])
            check_result = {'server_name':self.params["ConnectionName"], 
             'state_date':date_time,  'previous_date':(self.helper.get_date_time)(connection_state["ChangeState"]), 
             'activity':is_success,  'server_type':dbms_type, 
             'error':test_connection_result["error"]}
        return check_result

    @log_method
    def get_connection_state_from_local_db(self, connection_state, is_success, date_time):
        if connection_state is None:
            self.local_db.add_dbms_connection_state(self.params["ConnectionId"], is_success, date_time)
        else:
            self.local_db.update_dbms_connection_state(self.params["ConnectionId"], is_success, date_time)
        return self.local_db.get_dbms_connection_state(self.params["ConnectionId"])

    @log_method
    def get_backup_settings(self, db_name, job_backup_type):
        db_instance = self.get_db_server_class_instance(job_backup_type)
        backup_data = self.get_initial_backup_name_and_type(db_instance, db_name, job_backup_type)
        backup_data = self.check_if_previous_backup_success_and_return_data(db_name, backup_data, job_backup_type)
        if backup_data["raise_type"] is None:
            backup_data = db_instance.get_name_and_type_for_backup(db_name, job_backup_type, backup_data["backup_name"])
        return backup_data

    @log_method
    def get_initial_backup_name_and_type(self, db_instance, db_name, job_backup_type):
        backup_data = {}
        backup_type = db_instance.get_current_backup_type(db_name, job_backup_type)
        backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], backup_type)
        backup_data.update({
         'backup_type': backup_type, 
         'backup_name': backup_name, 
         'raise_type': None, 
         'raise_data': None})
        return backup_data

    @log_method
    def check_if_previous_backup_success_and_return_data(self, db_name, backup_data, job_backup_type):
        prev_full_backup = self.helper.check_if_previous_backup_was_success(db_name, BACKUP_TYPES[FULL_BACKUP_CONST], self.local_db, self.params["JobId"])
        is_backup_first = prev_full_backup is None
        is_backup_full_and_first = backup_data["backup_type"] == FULL_BACKUP_CONST and is_backup_first
        if is_backup_full_and_first:
            backup_data["raise_type"] = FULL_AND_FIRST_BACKUP
            backup_data["raise_data"] = {'DatabaseName':db_name, 
             'CurrentBackupType':backup_data["backup_type"], 
             'JobBackupType':job_backup_type}
        else:
            if job_backup_type != backup_data["backup_type"]:
                backup_data["raise_type"] = PREVIOUS_BACKUP_HAS_FAILED
                backup_data["raise_data"] = {'DatabaseName':db_name, 
                 'CurrentBackupType':backup_data["backup_type"], 
                 'JobBackupType':job_backup_type}
        return backup_data

    @log_method
    def calculate_and_return_checksum_for_file(self, db_name, job_id):
        db_instance = self.get_db_server_class_instance(self.params["JobBackupType"])
        return db_instance.calculate_and_return_checksum_for_file(db_name, job_id)

    @log_method
    def check_if_mysql_schema_has_changed(self, database_data, job_id, path_to_backup, file_format, backup_at):
        db_instance = self.get_db_server_class_instance(self.params["JobBackupType"])
        return db_instance.check_if_mysql_schema_has_changed(database_data, job_id, path_to_backup, file_format, backup_at)

    @log_method
    def get_db_data(self):
        db_instance = self.get_db_server_class_instance()
        return db_instance.get_db_data()

    @log_method
    def get_dbms_settings_as_xml(self, dbms_connection):
        instance = self.get_db_server_class_instance()
        return instance.get_connection_settings_as_xml(dbms_connection)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/dbms.pyc
