
from datetime import datetime
from sqlbak.helpers.files import is_windows_path
from sqlbak.definitions import CONFIG
from sqlbak.logger import log_error, log_method
from sqlbak.dbms.mssql.main import MsSqlServer, sql_delimeter
from uuid import uuid4
import os
from sqlbak.helpers.permissons import try_set_owner_parent_folder, try_with_full_access_folder
from sqlbak.dbms.mssql.helper import get_sql_server_user

class MsSqlServerFull(MsSqlServer):

    @log_method
    def __init__(self, params=None):
        MsSqlServer.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        """

        :param db_name:
        :param path_to_backup:
        :param backup_name:
        :return:
        """
        self.handle_offline_database(db_data["DatabaseName"])
        backup_params = self.get_backup_params(db_data["DatabaseName"], db_data["BackupName"], db_data["BackupExtension"], path_to_backup)
        self.create_backup(backup_params)
        self.verify_after_backup(backup_params["path_to_backup"])

    @log_method
    def get_backup_params(self, db_name, backup_name, backup_extention, path_to_backup):
        native_compression = self.get_native_compression()
        return {'name':("Backup. JobName: {0}. JobId: {1}. BackupId: {2}".format)(self.params["JobName"][None[:40]], self.params["JobId"], self.params["BackupId"]), 
         'backup_type':self.params["BackupType"], 
         'db_name':db_name, 
         'backup_name':backup_name, 
         'is_check_sum_enabled':"CHECKSUM," if (self.params["MS_EnableCheckSum"]) else "", 
         'is_backup_copy_only':"COPY_ONLY," if (self.params["MS_IsCopyOnly"]) else "", 
         'native_compression':native_compression, 
         'path_to_backup':(path_to_backup + backup_name) + backup_extention}

    @log_method
    def create_backup(self, params):
        sql = 'BACKUP DATABASE [{0}] TO DISK = "{1}" WITH {2} {3} {4} DESCRIPTION = "{5}", NAME = "{6}";'
        cmd = sql.format(params["db_name"], params["path_to_backup"], params["native_compression"], params["is_backup_copy_only"], params["is_check_sum_enabled"], CONFIG["MSSQL_BACKUP_DESC"], params["name"])
        try_set_owner_parent_folder(get_sql_server_user(), params["path_to_backup"])
        res = try_with_full_access_folder((lambda: self.make_tcp_request(" -Q '{0}'".format(cmd))))
        if "BACKUP DATABASE is terminating abnormally" in res:
            if "BACKUP DATABASE successfully processed" not in res:
                raise Exception(self.cm["FAILED_BACKUP_DBMS"].format(params["db_name"], res))

    @log_method
    def restore(self, restore_data):
        try:
            try_set_owner_parent_folder(get_sql_server_user(), restore_data["path_to_backup"])
            new_db_name = restore_data["backup"]["NewDatabaseName"]
            old_db_name = restore_data["backup"]["OldDatabaseName"]
            sql_settings = restore_data["backup"]["LocalSqlServerSettings"]
            if sql_settings is not None and sql_settings["VerifyOnly"]:
                self.check_restore_backup_verify_only(restore_data["path_to_backup"])
            else:
                recovery_mode = "RECOVERY" if restore_data["is_last_backup"] else "NORECOVERY"
                is_new_db = new_db_name not in self.get_databases_names()
                self.set_single_user(new_db_name)
                self.restore_full(new_db_name, restore_data["path_to_backup"], old_db_name, recovery_mode, is_new_db, sql_settings)
                if restore_data["is_last_backup"] and sql_settings is not None and sql_settings["CheckAfterRestore"]:
                    self.check_after_restore(new_db_name)
        except Exception as e:
            try:
                raise Exception(e)
            finally:
                e = None
                del e

        else:
            if restore_data["is_last_backup"]:
                self.set_multi_user(new_db_name)

    @log_method
    def get_all_database_files(self):
        query = "select db_name([dbid]),'{0}',[name],'{0}',[filename],'{0}',[groupid] from sysaltfiles".format(sql_delimeter)
        res = self.make_tcp_request('-Q "{0}" -h -1 -W -s \'\''.format(query, sql_delimeter))
        result_table = [x.split(sql_delimeter) for x in res.split("\n") if x != ""]
        return {x[2]: {'db_name':x[0],  'Name':x[1],  'Path':x[2],  'Type':x[0]} for x in result_table[None[:-1]]}

    @log_method
    def get_database_files_from_backup(self, path_to_backup):
        try_set_owner_parent_folder(get_sql_server_user(), path_to_backup)
        query = 'RESTORE FILELISTONLY FROM DISK = "{0}"'.format(path_to_backup)
        res = try_with_full_access_folder((lambda: self.make_tcp_request("-Q '{0}' -h -1 -W -s '{1}'".format(query, "|"))))
        result_table = [x.split("|") for x in res.split("\n") if x != ""]
        return [{'Name':x[0],  'Path':x[1],  'Type':0 if (x[2] == "L") else 1} for x in result_table[None[:-1]]]

    @log_method
    def gen_new_pathParse error at or near `LOAD_GLOBAL' instruction at offset 0

    @log_method
    def get_with_move_statementParse error at or near `LOAD_FAST' instruction at offset 0

    @log_method
    def restore_full(self, new_db_name, path_to_backup, old_db_name, recovery_mode, is_new_db, sql_settings):
        self.set_single_user(new_db_name)
        cmd = 'RESTORE DATABASE [{0}] FROM DISK = "{1}" WITH {2} REPLACE, {3};'.format(new_db_name, path_to_backup, self.get_with_move_statement(new_db_name, path_to_backup, sql_settings), recovery_mode)
        res = try_with_full_access_folder((lambda: self.make_tcp_request("-Q '{0}'".format(cmd))))
        if recovery_mode == "RECOVERY":
            self.set_multi_user(new_db_name)
        if "State" in res:
            raise Exception(self.cm["FAILED_RESTORE_DBMS"].format(new_db_name, res))

    @log_method
    def get_path_to_property_from_server(self, property, new_db_name=''):
        cmd = 'select serverproperty("{0}")'.format(property)
        res = self.make_tcp_request("-k -h -1 -W -Q '{0}'".format(cmd))
        if "State" in res:
            raise Exception(self.cm["FAILED_RESTORE_DBMS"].format(new_db_name, res))
        split_res = res.split()
        return split_res[0]

    @log_method
    def get_path_and_logical_names_from_sql_settings(self, sql_settings):
        file_names = None
        if sql_settings is not None:
            if len(sql_settings["Files"]) > 0:
                file_names = {}
                for f in sql_settings["Files"]:
                    file_names[f["Name"]] = {'Name':f["Name"], 
                     'Path':f["Path"], 
                     'Type':f["Type"]}

        return file_names
