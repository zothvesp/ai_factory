from sqlbak.logger import log_method
from sqlbak.dbms.xtrabackup.main import XtrabackupMain
from sqlbak.definitions import INC_BACKUP_CONST, BACKUP_TYPES, XTRABACKUP_CONST
from sqlbak.dbms.xtrabackup.full import XtrabackupFull

class XtrabackupInc(XtrabackupMain):

    @log_method
    def __init__(self, params=None):
        XtrabackupMain.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        password = self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None
        path_to_backup_with_name = path_to_backup + db_data["BackupName"]
        path_to_backup_copy = db_data["BackupWorkingDir"] + db_data["BackupName"]
        cmd = '{7} --host={0} --port={1} --user={2} --password=\'{3}\' --backup --databases "{6}" --target-dir={4} --incremental-basedir={5}'.format(self.params["Host"], self.params["Port"], self.params["User"], password, path_to_backup_with_name, db_data["PathToPreviousBackup"], db_data["DatabaseName"], self.utils["xtrabackup-path"])
        res = self.native_command.run_linux_script_with_password(cmd, [password] if password else [])
        self.native_command.copy_resource(path_to_backup_with_name, path_to_backup_copy)
        if db_data["PathToPreviousBackup"] is not None:
            self.helper.remove_file_or_dir([db_data["PathToPreviousBackup"]])
        self.local_db.save_current_backup_data(db_data["BackupJobId"], path_to_backup_copy, BACKUP_TYPES[INC_BACKUP_CONST], db_data["DatabaseName"], INC_BACKUP_CONST.lower()[0], XTRABACKUP_CONST, db_data["BackupId"])

    @log_method
    def restore(self, restore_data):
        try:
            script_result = ""
            password = self.helper.decrypt_string(self.params["Password"]) if self.params["Password"] else None
            if restore_data["is_first_backup"]:
                self.prepare_full_backup_to_restore(self.params["Host"], self.params["Port"], self.params["User"], password, restore_data["path_to_full_backup"])
            else:
                if restore_data["is_last_backup"]:
                    cmd = "{6} --host={0} --port={1} --user={2} --password='{3}' --prepare --target-dir={4} --incremental-dir={5}".format(self.params["Host"], self.params["Port"], self.params["User"], password, restore_data["path_to_full_backup"], restore_data["path_to_backup"], self.utils["xtrabackup-path"])
                    self.native_command.run_linux_script_with_password(cmd, [password] if password else [])
                    x_full = XtrabackupFull(self.params)
                    x_full.restore(restore_data)
                else:
                    cmd = "{6} --host={0} --port={1} --user={2} --password='{3}' --prepare --apply-log-only --target-dir={4} --incremental-dir={5}".format(self.params["Host"], self.params["Port"], self.params["User"], password, restore_data["path_to_full_backup"], restore_data["path_to_backup"], self.utils["xtrabackup-path"])
                    self.native_command.run_linux_script_with_password(cmd, [password] if password else [])
        except Exception as e:
            try:
                raise Exception(e)
            finally:
                e = None
                del e

    @log_method
    def prepare_full_backup_to_restore(self, host, port, user, password, path_to_backup):
        cmd = "{5} --host={0} --port={1} --user={2} --password='{3}' --prepare --apply-log-only --target-dir={4}".format(host, port, user, password, path_to_backup, self.utils["xtrabackup-path"])
        self.native_command.run_linux_script_with_password(cmd, [password] if password else [])

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/xtrabackup/inc.pyc
