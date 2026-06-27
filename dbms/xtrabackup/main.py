from sqlbak.logger import log_method
import os
from sqlbak.dbms.mysql.main import MySql
from sqlbak.definitions import FULL_BACKUP_CONST, INC_BACKUP_CONST, PREVIOUS_BACKUP_DOES_NOT_EXISTS

class XtrabackupMain(MySql):

    @log_method
    def __init__(self, params=None):
        MySql.__init__(self, params)

    @log_method
    def get_name_and_type_for_backup(self, db_name, backup_type, backup_name):
        backup_data = {'backup_type':backup_type, 
         'backup_name':backup_name, 
         'raise_type':None, 
         'raise_data':{'DatabaseName':db_name, 
          'CurrentBackupType':backup_type}}
        if backup_type == INC_BACKUP_CONST:
            if not self.check_if_previous_backup_exists(db_name):
                backup_name = self.helper.get_backup_file_name(self.params["FileNameFormat"], db_name, self.params["BackupAt"], FULL_BACKUP_CONST)
                backup_data.update({'backup_type':FULL_BACKUP_CONST, 
                 'backup_name':backup_name, 
                 'raise_type':PREVIOUS_BACKUP_DOES_NOT_EXISTS, 
                 'raise_data':{'CurrentBackupType':backup_type, 
                  'DatabaseName':db_name}})
        return backup_data

    @log_method
    def check_if_previous_backup_exists(self, db_name):
        last_success_backup = self.local_db.get_last_success_backup_data(self.params["JobId"], db_name)
        path_to_backup = last_success_backup["PathToBackup"] if last_success_backup is not None else None
        is_exists = path_to_backup is not None and os.path.exists(path_to_backup)
        return is_exists

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/xtrabackup/main.pyc
