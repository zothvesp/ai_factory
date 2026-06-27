import os
from datetime import datetime
import json
from sqlbak.definitions import CONFIG, BACKUP_TYPES, FULL_BACKUP_CONST, MYSQL_CONST, INC_BACKUP_CONST, DOCKER_EXEC, SUDO_SQLBAK
from sqlbak.dbms.mysql.main import MySql
from sqlbak.logger import log_data, log_error, log_method, log_only_exception
from sqlbak.helpers.temporary_directory import create_directory
from sqlbak.dbms.mysql.inc_helper import take_inc_backup
import sqlbak.config.log_settings, re

class MySqlInc(MySql):

    @log_method
    def __init__(self, params=None):
        MySql.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        if not self.is_bin_log_enabled():
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            raise Exception(self.cm["BIN_LOG_DISABLED"].format(self.params["ConnectionId"], msg_param))
        elif not self.is_row_format_enabled():
            is_app_run_in_docker = self.helper.is_app_run_in_docker_container()
            host_name = self.helper.get_host_name()
            msg_param = DOCKER_EXEC.format(host_name) if is_app_run_in_docker else SUDO_SQLBAK
            raise Exception(self.cm["ROW_FORMAT_DISABLED"].format(self.params["ConnectionId"], msg_param))
        if self.is_galera() and self.get_variable_value("log_slave_updates") != "ON":
            raise Exception(self.cm["LOG_SLAVE_UPDATES_DISABLED"].format(self.params["ConnectionId"]))
        take_inc_backup(self.params["JobId"], path_to_backup + db_data["BackupName"], self.params["BackupId"], self)

    @log_only_exception
    def save_bin_log_data(self, db_name, path_to_lib, bin_file, first_bin_log_index, path_to_backup, last_bin_log_index):
        split_name = bin_file.strip().split("/")
        file_name = str(split_name[-1])
        split_file_name = file_name.strip().split(".")
        file_index = int(str(split_file_name[-1]))
        if file_index >= int(first_bin_log_index):
            if file_index <= int(last_bin_log_index):
                path_to_bin_file = path_to_lib + file_name
                self.native_command.copy_resource(path_to_bin_file, path_to_backup)

    @log_method
    def rotate_bin_log(self):
        try:
            self.make_tcp_request("mysqladmin", "flush-logs")
        except Exception as ex:
            try:
                log_error(ex, "Can't flush log by mysqladmin. Try Flush log by FLUSH BINARY LOGS comand")
                self.make_tcp_request(self.utils["mysql-path"], "-e 'FLUSH BINARY LOGS;'")
            finally:
                ex = None
                del ex

    @log_method
    def get_start_binlog_from_fullParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def restore(self, restore_data):
        try:
            try:
                new_db_name = restore_data["backup"]["NewDatabaseName"]
                old_db_name = restore_data["backup"]["OldDatabaseName"]
                if restore_data["is_second_backup"]:
                    first_binlog = self.get_start_binlog_from_full(restore_data["path_to_full_backup"])
                else:
                    first_binlog = None
                path_to_decoded_log_backup = self.get_data_from_bin_log_files(restore_data["path_to_backup"], old_db_name, new_db_name, first_binlog)
                self.restore_log_backup(old_db_name, new_db_name, path_to_decoded_log_backup)
            except Exception as e:
                try:
                    raise Exception(e)
                finally:
                    e = None
                    del e

        finally:
            self.local_db.reset_backuped_binlog(self.get_path_to_log_bin_index())

    @log_method
    def get_data_from_bin_log_files(self, path_to_backup, old_db_name, new_db_name, first_binlog):
        bin_log_files = sorted(self.helper.get_files_in_directory(path_to_backup))
        decoded_file_name = path_to_backup + "/binlogs." + new_db_name + ".decoded.sql"
        if first_binlog is not None:
            bin_log_files = [x for x in bin_log_files if x >= first_binlog]
        additional_argument = sqlbak.config.log_settings.mysqlbinlog_additional_arguments
        if self.mysqlbinlog_is_support_parameter("no-defaults"):
            additional_argument += " --no-defaults "
        if self.is_galera():
            additional_argument += " --disable-log-bin "
        for idx, bin_log_file in enumerate(bin_log_files):
            if new_db_name == old_db_name:
                cmd = " {0} {1} --database='{2}' {3} {4}".format(path_to_backup + "/" + bin_log_file, additional_argument, old_db_name, ">" if idx == 0 else ">>", decoded_file_name)
            else:
                if self.is_maria_db():
                    cmd = " {0} {1} --database='{2}' --rewrite-db='{3}->db_something' --rewrite-db='{2}->{3}' {4} {5}".format(path_to_backup + "/" + bin_log_file, additional_argument, old_db_name, new_db_name, ">" if idx == 0 else ">>", decoded_file_name)
                else:
                    cmd = " {0} {1} --database='{3}' --rewrite-db='{3}->db_something' --rewrite-db='{2}->{3}' {4} {5}".format(path_to_backup + "/" + bin_log_file, additional_argument, old_db_name, new_db_name, ">" if idx == 0 else ">>", decoded_file_name)
            try:
                log_data("Try to decode binlog file {0}".format(bin_log_file))
                self.make_tcp_request("mysqlbinlog", cmd)
                log_data("Binlog file {0} decoded".format(bin_log_file))
            except Exception as e:
                try:
                    log_error(e, "Can't decode binlog file {0}".format(bin_log_file))
                    if "no-defaults" in str(e):
                        log_data("Try to decode binlog file {0} without --no-defaults parameter".format(bin_log_file))
                        cmd = cmd.replace("--no-defaults", "")
                        self.make_tcp_request("mysqlbinlog", cmd)
                    else:
                        raise Exception(e)
                finally:
                    e = None
                    del e

        else:
            return decoded_file_name

    @log_method
    def restore_log_backup(self, old_db_name, new_db_name, path_to_log_backup):
        try:
            self.make_tcp_request(self.utils["mysql-path"], "-e 'SET FOREIGN_KEY_CHECKS=0;'")
            cmd = ' -e "source {0}"'.format(path_to_log_backup)
            self.make_tcp_request(self.utils["mysql-path"], cmd)
            self.make_tcp_request(self.utils["mysql-path"], "-e 'SET FOREIGN_KEY_CHECKS=1;'")
            self.helper.remove_file_or_dir([path_to_log_backup])
        except Exception as e:
            try:
                self.helper.remove_file_or_dir([path_to_log_backup])
                raise Exception(e)
            finally:
                e = None
                del e

    def trace_binlog_file_name(self, file_name, size):
        self.job_log.sql_binlog_backuped(self.params, file_name, size)
