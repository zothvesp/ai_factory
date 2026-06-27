
import json
from datetime import datetime
from sqlbak.definitions import DIFF_BACKUP_CONST, SYSTEM_DATABASES_MSSQL, SEVERITY_PARAMS, LOG_BACKUP_CONST, BACKUP_TYPES, MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL, MSSQL_DOUBLE_LOG_SAME_MINUTE
from sqlbak.definitions import CONFIG, FULL_BACKUP_CONST, MSSQL_BACKUP_TYPES, BROKEN_BACKUP_BEHAVIOR, MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR, MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG, SQL_SCRIPT_TYPE
from sqlbak.helper import Helper
from sqlbak.local_db import LocalDB
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_error, log_method
from sqlbak.job_log import JobLog
from sqlbak.app_output import APP_OUTPUT
sql_delimeter = "ef34ad14-7074-493e-ada3-5eeaaf25442f"

class MsSqlServer:

    @log_method
    def __init__(self, params=None):
        self.helper = Helper()
        self.job_log = JobLog()
        self.params = params
        self.utils = json.loads(self.params["UtilsPath"])
        self.local_db = LocalDB()
        self.native_command = NativeCommand()
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def make_tcp_request(self, request=''):
        params = self.helper.get_params_to_run_server_script(self.utils["sqlcmd-path"], request, self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        return self.native_command.make_tcp_request_to_mssql(params)

    @log_method
    def get_databases_names(self):
        result = self.make_tcp_request("-Q 'SELECT name FROM master.sys.databases;'")
        db_list = []
        if result:
            for d in result.split("\n")[2[:-3]]:
                db_list.append(d.strip())

        return db_list

    @log_method
    def get_db_data(self):
        try:
            q = "EXEC sp_MSForEachDB ' USE [?]; SELECT DB_NAME(),''{0}'', name,''{0}'', type,''{0}'', physical_name FROM sys.database_files WHERE type IN (0,1);'".format(sql_delimeter)
            databaes_info = self.make_tcp_request('-Q "{0}" -h -1 -W -s \'\''.format(q))
            splited_databaes_info = [x.split(sql_delimeter) for x in databaes_info.split("\n") if x != ""]
            paesed_databases_info = [{'db_name':x[0], 
             'logical_name':x[1],  'file_type':x[2],  'file_path':x[3]} for x in splited_databaes_info]
            databases_names = set([x["db_name"] for x in paesed_databases_info])
            database_data = [{'Name':db_name, 
             'Error':None, 
             'Files':[{'Name':db_info_row["logical_name"], 
              'Type':int(db_info_row["file_type"]), 
              'Path':db_info_row["file_path"]} for db_info_row in paesed_databases_info if db_info_row["db_name"] == db_name]} for db_name in databases_names]
            return             return {"Databases": database_data} if len(database_data) > 0 else None
            except Exception as e:
            try:
                log_error(e, "Cant read databases info")
                raise e
            finally:
                e = None
                del e

    @log_method
    def get_non_system_databases(self):
        return [database for database in self.get_databases_names() if database not in SYSTEM_DATABASES_MSSQL]

    @log_method
    def test_db_connectionParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def handle_scripts(self, script, timeout):
        """

        :param script:
        :param timeout:
        :return:
        """
        if "CountJobErrors" in self.params:
            job_success_variable = 0 if self.params["CountJobErrors"] > 0 else 1
            backup_type_varriable = self.params["BackupType"]
            joined_script = "DECLARE @SQLBAK_JOB_SUCCESS int = {0}; DECLARE @SQLBAK_BACKUP_TYPE varchar(10) = '{1}';".format(job_success_variable, backup_type_varriable) + "".join(script)
        else:
            joined_script = "".join([x for x in script if x])
        params = self.helper.get_params_to_run_server_script(self.utils["sqlcmd-path"], '-Q "{0};"'.format(joined_script), self.params["Password"], self.params["Port"], self.params["UseSsh"], self.params["SshHost"], self.params["SshUser"], self.params["SshPassword"], self.params["Host"], self.params["User"], self.params["SshPort"], self.params["SshLocalMappedPort"])
        res = self.helper.run_method_with_number_attempts_and_timeout(NativeCommand, "make_tcp_request_to_mssql", params=(params,), attempts=1, time_out=timeout)
        if "State" in res:
            raise Exception(self.cm["FAILED_VERIFY_AFTER_BACKUP"].format(res))
        return res

    @log_method
    def handle_offline_database(self, db_name):
        ignore_offline_database = self.params["DatabaseState"] is not None
        if not ignore_offline_database:
            is_database_offline = self.check_if_database_is_offline(db_name)
            if is_database_offline:
                raise Exception(self.cm["DB_OFFLINE"].format(db_name))

    @log_method
    def get_native_compression(self):
        if self.params["MS_NativeBackupCompression"] is None:
            native_compression = ""
        else:
            native_compression = "COMPRESSION," if self.params["MS_NativeBackupCompression"] == "Compress" else "NO_COMPRESSION,"
        return native_compression

    @log_method
    def get_name_and_type_for_backup(self, db_name, backup_type, backup_name):
        backup_data = {'backup_type':backup_type, 
         'backup_name':backup_name, 
         'raise_type':None, 
         'raise_data':{'DatabaseName':db_name, 
          'CurrentBackupType':backup_type}}
        is_chain_broken = False
        if backup_type != FULL_BACKUP_CONST:
            is_chain_broken = self.check_if_backup_chain_is_broken(db_name, backup_type)
        elif is_chain_broken:
            if self.params["BrokenChainBehavior"] == BROKEN_BACKUP_BEHAVIOR["ERROR"]:
                backup_data["raise_type"] = MSSQL_BACKUP_CHAIN_BROKEN_RAISE_ERROR
            else:
                if self.params["BrokenChainBehavior"] == BROKEN_BACKUP_BEHAVIOR["WARNING"]:
                    backup_data["raise_type"] = MSSQL_BACKUP_CHAIN_BROKEN_RAISE_WARNINIG
                else:
                    backup_type = FULL_BACKUP_CONST
                    backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], backup_type)
                    backup_data.update({'backup_type':backup_type, 
                     'backup_name':backup_name, 
                     'raise_type':MSSQL_BACKUP_CHAIN_BROKEN_MAKE_FULL})
        else:
            if backup_type == LOG_BACKUP_CONST:
                if self.check_if_log_backup_is_double_backup_same_time(db_name):
                    backup_type = FULL_BACKUP_CONST
                    backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], backup_type)
                    backup_data.update({'backup_type':backup_type, 
                     'backup_name':backup_name, 
                     'raise_type':MSSQL_DOUBLE_LOG_SAME_MINUTE})
        return backup_data

    @log_method
    def verify_after_backup(self, path_to_backup):
        """

        :param path_to_backup:
        :return:
        """
        if self.params["MS_VerifyAfterBackup"]:
            cmd = 'RESTORE VERIFYONLY FROM DISK = "{0}"'.format(path_to_backup)
            res = self.make_tcp_request(" -Q '{0}'".format(cmd))
            if "State" in res:
                raise Exception(self.cm["FAILED_VERIFY_AFTER_BACKUP"].format(res))

    @log_method
    def check_if_database_is_offline(self, db_name):
        """

        :param db_name:
        :return:
        """
        data = self.get_data_if_database_is_offline(db_name)
        self.check_data_if_database_is_offline(data, db_name)

    @log_method
    def get_data_if_database_is_offline(self, db_name):
        cmd = 'SELECT DATABASEPROPERTYEX("{0}", "STATUS");'.format(db_name)
        res = self.make_tcp_request(" -Q '{0}'".format(cmd))
        if "State" in res:
            raise Exception(self.cm["FAILED_DB_OFFLINE"].format(db_name, res))
        return res

    @log_method
    def check_data_if_database_is_offline(self, data, db_name):
        split_result = data.split()
        if len(split_result) > 1:
            return split_result[1] != "ONLINE"
        raise Exception(self.cm["FAILED_DB_OFFLINE"].format(db_name, data))

    @log_method
    def check_if_backup_chain_is_broken(self, db_name, backup_type):
        """

        :param db_name:
        :param backup_type:
        :return:
        """
        native_backup_type = MSSQL_BACKUP_TYPES["FULL"] if backup_type == DIFF_BACKUP_CONST else None
        is_last_backup_done_by_the_app = self.is_last_backup_type_done_by_sqlbak(db_name, CONFIG["MSSQL_BACKUP_DESC"], native_backup_type)
        count_full_backups = self.get_count_full_backups(db_name)
        return not is_last_backup_done_by_the_app and count_full_backups > 0

    @log_method
    def is_last_backup_type_done_by_sqlbak(self, db_name, description, backup_type=None):
        """

        :param db_name:
        :param backup_type:
        :param description:
        :return:
        """
        backup_param = 'and [msdb].[dbo].[backupset].[type] = "{0}"'.format(backup_type) if backup_type is not None else ""
        cmd = 'SELECT top 1 [msdb].[dbo].[backupset].[description] as Description\n                FROM [msdb].[dbo].[backupmediafamily]\n                INNER JOIN [msdb].[dbo].[backupset] ON [msdb].[dbo].[backupmediafamily].[media_set_id] = [msdb].[dbo].[backupset].[media_set_id]\n                where [msdb].[dbo].[backupset].[is_copy_only] = 0 and [msdb].[dbo].[backupset].[database_name] = "{0}"\n                {1}  ORDER BY [msdb].[dbo].[backupset].[backup_finish_date] DESC'.format(db_name, backup_param)
        res = self.make_tcp_request(" -Q '{0}'".format(cmd))
        split_result = res.split()
        return len(split_result) > 2 and split_result[2] + " " + split_result[3] == description

    @log_method
    def get_count_full_backups(self, db_name: str):
        """

        :param db_name:
        :return:
        """
        cmd = 'SELECT COUNT(*) as COUNT\n                 FROM [msdb].[dbo].[backupmediafamily]\n                 INNER JOIN [msdb].[dbo].[backupset] ON [msdb].[dbo].[backupmediafamily].[media_set_id] = [msdb].[dbo].[backupset].[media_set_id]\n                 WHERE [msdb].[dbo].[backupset].[database_name] = "{0}" \n                 and [msdb].[dbo].[backupset].[type] = "D" '.format(db_name)
        res = self.make_tcp_request(" -Q '{0}'".format(cmd))
        split_result = res.split()
        return int(split_result[2])

    @log_method
    def set_single_user(self, db_name):
        self.make_tcp_request("-Q 'ALTER DATABASE [{0}] SET SINGLE_USER;'".format(db_name))

    @log_method
    def set_multi_user(self, db_name):
        self.make_tcp_request("-Q 'ALTER DATABASE [{0}] SET MULTI_USER;'".format(db_name))

    @log_method
    def get_current_backup_type(self, db_name, backup_type):
        if backup_type == LOG_BACKUP_CONST:
            last_backup_type = self.local_db.get_last_backup_type_for_job_id(self.params["JobId"])
            backup_type = backup_type if (last_backup_type is not None and self.helper.check_if_previous_backup_was_success(db_name, last_backup_type, self.local_db, self.params["JobId"])) else FULL_BACKUP_CONST
        else:
            backup_type = DIFF_BACKUP_CONST if (backup_type == DIFF_BACKUP_CONST and self.helper.check_if_previous_backup_was_success(db_name, BACKUP_TYPES[FULL_BACKUP_CONST], self.local_db, self.params["JobId"])) else FULL_BACKUP_CONST
        return backup_type

    @log_method
    def check_if_log_backup_is_double_backup_same_time(self, db_name):
        is_same_minute = False
        last_log_backup_time = self.local_db.get_time_of_last_log_backup_for_a_job(self.params["JobId"], db_name)
        if last_log_backup_time is not None:
            last_log_backup_time = self.helper.get_date_time(last_log_backup_time)
            now = datetime.now()
            is_same_minute = now.year == last_log_backup_time.year and now.month == last_log_backup_time.month and now.day == last_log_backup_time.day and now.hour == last_log_backup_time.hour and now.minute == last_log_backup_time.minute
        return is_same_minute

    @log_method
    def check_restore_backup_verify_only(self, path_to_backup):
        res = self.make_tcp_request('-Q \'RESTORE VERIFYONLY FROM DISK = "{0}";\''.format(path_to_backup))
        if "State" in res:
            raise Exception(res)

    @log_method
    def check_after_restore(self, db_name):
        res = self.make_tcp_request("-Q 'DBCC CHECKDB ([{0}]) WITH NO_INFOMSGS;'".format(db_name))
        if "State" in res:
            raise Exception(res)

    @log_method
    def get_connection_settings_as_xml(self, dbms_connection):
        return "<DatabaseConnectionInfo Server='{0}' UserName='{1}' Password='{2}' IntegratedSecurity='True' Timeout='180' />".format(self.helper.check_none(dbms_connection["Host"]), self.helper.check_none(dbms_connection["User"]), self.helper.check_none(dbms_connection["Password"]))

    def set_single_user(self, db_name):
        if db_name in self.get_databases_names():
            res = self.make_tcp_request("-Q 'ALTER DATABASE [{0}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;'".format(db_name))
            if "State" in res:
                raise Exception(res)

    def set_multi_user(self, db_name):
        if db_name in self.get_databases_names():
            res = self.make_tcp_request("-Q 'ALTER DATABASE [{0}] SET MULTI_USER;'".format(db_name))
            if "State" in res:
                raise Exception(res)
