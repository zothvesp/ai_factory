from sqlbak.definitions import CONFIG, MINUTE_IN_SEC, FULL_BACKUP_CONST, LOG_BACKUP_CONST
from sqlbak.logger import log_method
from sqlbak.dbms.mssql.main import MsSqlServer
from sqlbak.helpers.permissons import try_set_owner_parent_folder, try_with_full_access_folder
from sqlbak.dbms.mssql.helper import get_sql_server_user

class MsSqlServerLog(MsSqlServer):

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
        try_set_owner_parent_folder(get_sql_server_user(), params["path_to_backup"])
        sql = 'BACKUP {7} [{0}] TO DISK = "{1}" WITH {2} {3} {4} DESCRIPTION = "{5}", NAME = "{6}";'
        cmd = sql.format(params["db_name"], params["path_to_backup"], params["native_compression"], params["is_backup_copy_only"], params["is_check_sum_enabled"], CONFIG["MSSQL_BACKUP_DESC"], params["name"], "DATABASE" if params["backup_type"] == FULL_BACKUP_CONST else "LOG")
        res = try_with_full_access_folder((lambda: self.make_tcp_request(" -Q '{0}'".format(cmd))))
        if "BACKUP LOG is terminating abnormally" in res:
            if "BACKUP LOG successfully processed" not in res:
                raise Exception(self.cm["FAILED_BACKUP_DBMS"].format(params["db_name"], res))

    @log_method
    def restore(self, restore_data):
        try:
            try_set_owner_parent_folder(get_sql_server_user(), restore_data["path_to_backup"])
            new_db_name = restore_data["backup"]["NewDatabaseName"]
            sql_settings = restore_data["backup"]["LocalSqlServerSettings"]
            if sql_settings is not None and sql_settings["VerifyOnly"]:
                self.check_restore_backup_verify_only(restore_data["path_to_backup"])
            else:
                recovery_mode = "RECOVERY" if restore_data["is_last_backup"] else "NORECOVERY"
                cmd = 'RESTORE LOG [{0}] FROM DISK = "{1}" WITH {2};'.format(new_db_name, restore_data["path_to_backup"], recovery_mode)
                res = try_with_full_access_folder((lambda: self.make_tcp_request(" -Q '{0}'".format(cmd))))
                if "State" in res:
                    raise Exception(self.cm["FAILED_TRANS_RESTORE"].format(new_db_name, res))
                if recovery_mode == "RECOVERY":
                    self.set_multi_user(new_db_name)
                if restore_data["is_last_backup"] and sql_settings is not None and sql_settings["CheckAfterRestore"]:
                    self.check_after_restore(new_db_name)
        except Exception as e:
            try:
                raise Exception(e)
            finally:
                e = None
                del e

        if restore_data["is_last_backup"]:
            self.set_multi_user(new_db_name)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/mssql/log.pyc
