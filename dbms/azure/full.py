import os
from sqlbak.logger import log_method
from sqlbak.dbms.azure.main import AzureMain
from sqlbak.definitions import FULL_BACKUP_CONST, BACKUP_TYPES
from sqlbak.job_log import JobLog

class AzureFull(AzureMain):

    @log_method
    def __init__(self, params=None):
        self.job_log = JobLog()
        AzureMain.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        path_to_database_backup = path_to_backup + db_data["BackupName"] + db_data["BackupExtension"]
        db_name = db_data["DatabaseName"]
        if self.params["Azure_CreateSnapshot"]:
            snapshot_name = db_name + "_sqlbak_snapshot"
            try:
                azure_configuration = self.get_azure_configuration(db_name)
                self.job_log.create_azure_snapshot(self.params, db_name, snapshot_name)
                self.create_azure_database(snapshot_name, db_name, azure_configuration)
                self.job_log.export_azure_database(self.params, snapshot_name, db_data["BackupExtension"])
                self.export_attempts(snapshot_name, path_to_database_backup, 1200)
            finally:
                if snapshot_name in self.get_databases_names():
                    self.job_log.drop_azure_snapshot(self.params, snapshot_name)
                    self.drop_database(snapshot_name)

        else:
            self.job_log.export_azure_database(self.params, db_name, db_data["BackupExtension"])
            self.make_sqlpackage_request_export(' /SourceDatabaseName:"{0}" /TargetFile:"{1}" '.format(db_name, path_to_database_backup))

    @log_method
    def restore(self, restore_data):
        path_to_backup = restore_data["path_to_backup"]
        new_db_name = restore_data["backup"]["NewDatabaseName"]
        old_db_name = restore_data["backup"]["OldDatabaseName"]
        temp_database = new_db_name + "_sqlbak_temp_restore"
        try:
            try:
                azure_configuration = self.get_azure_configuration(old_db_name)
                if new_db_name in self.get_databases_names():
                    self.create_azure_database(temp_database, None, azure_configuration)
                    self.make_sqlpackage_request_import(' /TargetDatabaseName:"{0}" /SourceFile:"{1}" '.format(temp_database, path_to_backup))
                    self.drop_database(new_db_name)
                    self.rename_database(temp_database, new_db_name)
                else:
                    self.create_azure_database(new_db_name, None, azure_configuration)
                    self.make_sqlpackage_request_import(' /TargetDatabaseName:"{0}" /SourceFile:"{1}" '.format(new_db_name, path_to_backup))
            except Exception as e:
                try:
                    raise Exception(e)
                finally:
                    e = None
                    del e

        finally:
            if temp_database in self.get_databases_names():
                self.drop_database(temp_database)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/azure/full.pyc
