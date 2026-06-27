import os
from sqlbak.logger import log_method, log_data
from sqlbak.dbms.mysql.main import MySql
from sqlbak.exceptions import MySQLDumpError
from sqlbak.dbms.mysql.inc_helper import get_last_binlog
from sqlbak.app_output import APP_OUTPUT
from sqlbak.definitions import CONFIG, DOCKER_EXEC, KNOWLEDGE_BASE_LINKS, SUDO_SQLBAK

class MySqlFull(MySql):

    @log_method
    def __init__(self, params=None):
        MySql.__init__(self, params)
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def backup_database(self, db_data, path_to_backup):
        """

        :param db_name:
        :param path_to_database_backup:
        :return:
        """
        try:
            last_bin_log = None
            path_to_index = None
            if db_data["IsIncBackupEnabled"]:
                if self.is_bin_log_enabled():
                    if self.is_row_format_enabled():
                        path_to_lib = self.get_path_to_logs_lib()
                        path_to_index = self.get_path_to_log_bin_index()
                        if path_to_lib is None:
                            raise Exception(self.cm["FAILED_GET_LIB_DIR_MYSQL"])
                        if path_to_index is None:
                            raise Exception(self.cm["BINLOG_INDEX_NOT_FOUND"])
                        if not os.path.exists(path_to_index):
                            if self.params["Host"] == "localhost" or self.params["Host"] == "127.0.0.1":
                                raise Exception(self.cm["BINLOG_INDEX_NOT_PATH_FOUND"].format(path_to_index))
                            else:
                                raise Exception(KNOWLEDGE_BASE_LINKS["INC_BACKUP_NOT_SUPPORTED_FOR_REMOTE_MYSQL"]["code"] + " " + self.cm["BINLOG_INDEX_NOT_PATH_FOUND_REMOUTE"].format(path_to_index))
                        last_bin_log = get_last_binlog(path_to_index)
                        if last_bin_log is None:
                            raise Exception(self.cm["LAST_BINLOG_NOT_FOUND"])
            path_to_database_backup = path_to_backup + db_data["BackupName"] + db_data["BackupExtension"]
            optional_parameters = self.get_optional_parameters()
            if self.is_bin_log_enabled():
                if self.is_row_format_enabled():
                    if db_data["IsIncBackupEnabled"]:
                        optional_parameters.append("--flush-logs")
                    elif self.mysqldump_is_support_parameter("source-data"):
                        optional_parameters.append("--source-data=2")
                    else:
                        optional_parameters.append("--master-data=2")
            self.make_tcp_request(self.utils["mysqldump-path"], ' --databases "{1}" --result-file="{2}" {0} '.format(" ".join(optional_parameters), db_data["DatabaseName"], path_to_database_backup))
            if self.params["My_SQLHeaderComment"]:
                comments = ["-- " + comment.strip() + "\\n" for comment in self.params["My_SQLHeaderComment"].split("\\n")]
                self.native_command.add_text_to_beginning_file("".join(comments), path_to_database_backup)
            if self.params["My_SqlIfNotExists"]:
                self.native_command.replace_substring_in_file("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", path_to_database_backup)
            if db_data["IsIncBackupEnabled"]:
                if self.is_bin_log_enabled():
                    if not self.is_row_format_enabled():
                        is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
                        host_name = self.helper.get_host_name()
                        msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
                        raise Exception(self.cm["ROW_FORMAT_DISABLED"].format(self.params["ConnectionId"], msg_param))
                    prev = self.local_db.get_last_backuped_binlog(path_to_index, self.params["JobId"])
                    if len(prev) > 0 and prev[0]["BackupId"] == self.params["BackupId"]:
                        log_data("Binlog already saved. BackupId: " + str(self.params["BackupId"]) + " JobId: " + str(self.params["JobId"]) + " Path: " + path_to_index)
                else:
                    self.local_db.save_backuped_binlog(path_to_index, self.params["JobId"], last_bin_log, self.params["BackupId"])
        except Exception as e:
            try:
                raise MySQLDumpError(e)
            finally:
                e = None
                del e

    @log_method
    def restore(self, restore_data):
        try:
            try:
                new_db_name = restore_data["backup"]["NewDatabaseName"]
                old_db_name = restore_data["backup"]["OldDatabaseName"]
                path_to_backup = restore_data["path_to_backup"]
                if not self.is_galera():
                    disable_log_bin_text = "/*!40101 SET SESSION SQL_LOG_BIN=0 */;"
                    try:
                        self.make_tcp_request(self.utils["mysql-path"], "-e '{0}'".format(disable_log_bin_text))
                    except:
                        disable_log_bin_text = ""
                        self.native_command.remove_line_in_file("SET @@SESSION.SQL_LOG_BIN=", path_to_backup)
                        self.native_command.remove_line_in_file("SET @@GLOBAL.GTID_PURGED=", path_to_backup)

                else:
                    disable_log_bin_text = ""
                self.native_command.add_text_to_beginning_file("\\/*!40101 SET FOREIGN_KEY_CHECKS=0 *\\/;" + disable_log_bin_text.replace("/", "\\/"), path_to_backup)
                self.make_tcp_request(self.utils["mysql-path"], "-e '/*!40101 SET FOREIGN_KEY_CHECKS=0 */; {0} DROP DATABASE IF EXISTS `{1}`;'".format(disable_log_bin_text, str(new_db_name)))
                self.make_tcp_request(self.utils["mysql-path"], "-e '{0} CREATE DATABASE `{1}`;'".format(disable_log_bin_text, str(new_db_name)))
                if new_db_name != old_db_name:
                    self.native_command.cut_substring_in_file("CREATE DATABASE", path_to_backup)
                    self.native_command.cut_substring_in_file("USE `{0}`;".format(old_db_name), path_to_backup)
                self.make_tcp_request(self.utils["mysql-path"], ' "{0}" < {1} '.format(new_db_name, path_to_backup))
            except Exception as e:
                try:
                    raise Exception(e)
                finally:
                    e = None
                    del e

        finally:
            path_to_log_bin_index = self.get_path_to_log_bin_index()
            if path_to_log_bin_index:
                self.local_db.reset_backuped_binlog(path_to_log_bin_index)

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/mysql/full.pyc
