import os
from sqlbak.logger import log_method
from sqlbak.dbms.xtrabackup.main import XtrabackupMain
from sqlbak.definitions import FULL_BACKUP_CONST, BACKUP_TYPES, XTRABACKUP_CONST

class XtrabackupFull(XtrabackupMain):

    @log_method
    def __init__(self, params=None):
        XtrabackupMain.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        password = self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None
        path_to_backup_with_name = path_to_backup + db_data["BackupName"]
        path_to_backup_copy = db_data["BackupWorkingDir"] + db_data["BackupName"]
        cmd = '{4} --backup --user={0} --password=\'{1}\' --databases="{3}" --target-dir={2} --datadir={5}'.format(self.params["User"], password, path_to_backup_with_name, db_data["DatabaseName"], self.utils["xtrabackup-path"], self.utils["mysql-lib"])
        self.native_command.run_linux_script_with_password(cmd, [password] if password else [])
        self.native_command.copy_resource(path_to_backup_with_name, path_to_backup_copy)
        if db_data["PathToPreviousBackup"] is not None:
            self.helper.remove_file_or_dir([db_data["PathToPreviousBackup"]])
        self.local_db.save_current_backup_data(db_data["BackupJobId"], path_to_backup_copy, BACKUP_TYPES[FULL_BACKUP_CONST], db_data["DatabaseName"], FULL_BACKUP_CONST.lower()[0], XTRABACKUP_CONST, db_data["BackupId"])

    @log_method
    def restore(self, restore_data):
        try:
            print("restore")
            script_result = ""
            new_db_name = restore_data["backup"]["NewDatabaseName"]
            old_db_name = restore_data["backup"]["OldDatabaseName"]
            path_to_backup = restore_data["path_to_backup"]
            path_to_old_dir = "/var/lib/mysql.old/"
            password = self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None
            self.native_command.stop_mysql_service()
            print("restore1", new_db_name, old_db_name, path_to_backup)
            if restore_data["is_first_backup"]:
                print("restore2")
                cmd = "{5} --host={0} --port={1} --user={2} --password='{3}' --prepare --export --target-dir={4} --datadir={6}".format(self.params["Host"], self.params["Port"], self.params["User"], password, path_to_backup, self.utils["xtrabackup-path"], self.utils["mysql-lib"])
                self.native_command.run_linux_script_with_password(cmd, [password] if password else [])
            print("restore3")
            self.helper.remove_file_or_dir([path_to_old_dir + old_db_name])
            print("restore4")
            if not os.path.exists(path_to_old_dir):
                print("restore5")
                self.native_command.make_directory(path_to_old_dir)
                self.set_ownership_and_privilleges_to_resource(path_to_old_dir)
            print("restore6")
            if os.path.exists(self.utils["mysql-lib"] + "/" + old_db_name):
                print("restore7")
                self.native_command.move_resource(self.utils["mysql-lib"] + "/" + old_db_name, path_to_old_dir + old_db_name)
            print("restore8")
            self.native_command.move_resource(path_to_backup + "/" + old_db_name, self.utils["mysql-lib"] + "/" + old_db_name)
            self.set_ownership_and_privilleges_to_resource(self.utils["mysql-lib"])
            self.native_command.start_mysql_service()
        except Exception as e:
            try:
                print("restore10", str(e))
                raise Exception(e)
            finally:
                e = None
                del e

        else:
            print("restore11", script_result)
            return script_result

    @log_method
    def set_ownership_and_privilleges_to_resource(self, path_to_resource):
        cmd = "chown --preserve-root --no-dereference -R mysql:mysql {0}".format(path_to_resource)
        self.native_command.run_linux_script(cmd)
        cmd = "chmod --preserve-root -R 700 {0}".format(path_to_resource)
        self.native_command.run_linux_script(cmd)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/xtrabackup/full.pyc
