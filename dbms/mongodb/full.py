import os
from sqlbak.logger import log_method
from sqlbak.dbms.mongodb.main import MongoMain
from sqlbak.definitions import FULL_BACKUP_CONST, BACKUP_TYPES
from sqlbak.helpers.temporary_directory import clear_all_files_in_folder

class MongoDbFull(MongoMain):

    @log_method
    def __init__(self, params=None):
        MongoMain.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        path_to_database_backup = path_to_backup + db_data["BackupName"]
        try:
            self.make_tcp_request(self.utils["mongodump-path"], ' --db "{0}" --forceTableScan --out "{1}" --authenticationDatabase "{2}" '.format(db_data["DatabaseName"], path_to_database_backup, self.get_auth_database()))
        except:
            clear_all_files_in_folder(path_to_database_backup)
            self.make_tcp_request(self.utils["mongodump-path"], ' --db "{0}" --forceTableScan --out "{1}" '.format(db_data["DatabaseName"], path_to_database_backup))

    @log_method
    def restore(self, restore_data):
        try:
            script_result = ""
            new_db_name = restore_data["backup"]["NewDatabaseName"]
            old_db_name = restore_data["backup"]["OldDatabaseName"]
            path_to_backup = restore_data["path_to_backup"]
            try:
                self.make_tcp_request(self.utils["mongorestore-path"], ' --db "{0}" --quiet --drop --dir "{1}" --authenticationDatabase "{2}" '.format(new_db_name, path_to_backup + "/" + old_db_name, self.get_auth_database()))
            except:
                self.make_tcp_request(self.utils["mongorestore-path"], ' --db "{0}" --quiet --drop --dir "{1}" '.format(new_db_name, path_to_backup + "/" + old_db_name))

        except Exception as e:
            try:
                raise Exception(e)
            finally:
                e = None
                del e

        else:
            return script_result

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/mongodb/full.pyc
