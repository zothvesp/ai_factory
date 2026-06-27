from sqlbak.native_command import native_command_instanse
from sqlbak.logger import log_method
from sqlbak.dbms.postgres.main import PostgreSql

class PostgreSqlFull(PostgreSql):

    @log_method
    def __init__(self, params=None):
        PostgreSql.__init__(self, params)

    @log_method
    def backup_database(self, db_data, path_to_backup):
        """
        Method to make a backup of a db
        :return: None
        """
        optional_params = self.get_optional_params(self.utils["psql-path"], " -V")
        self.make_tcp_request(self.utils["pgdump-path"], ' {0} "{1}" > {2} '.format(" ".join(optional_params), db_data["DatabaseName"], path_to_backup + db_data["BackupName"] + db_data["BackupExtension"]))

    @log_method
    def restore(self, restore_data):
        try:
            new_db_name = restore_data["backup"]["NewDatabaseName"]
            old_db_name = restore_data["backup"]["OldDatabaseName"]
            formatted_new_db_name = '\\"' + str(new_db_name) + '\\"' if self.params["User"] == "postgres" and not self.params["Password"] else '"' + str(new_db_name) + '"'
            formatted_user = '\\"' + str(self.params["User"]) + '\\"' if self.params["User"] == "postgres" and not self.params["Password"] else '"' + str(self.params["User"]) + '"'
            self.make_tcp_request(self.utils["psql-path"], "-d postgres -c 'DROP DATABASE IF EXISTS {0} '".format(formatted_new_db_name))
            self.make_tcp_request(self.utils["psql-path"], "-d postgres -c 'CREATE DATABASE {0} OWNER {1} '".format(formatted_new_db_name, formatted_user))
            if new_db_name != old_db_name:
                self.native_command.cut_substring_in_file("CREATE DATABASE", restore_data["path_to_backup"])
                self.native_command.cut_substring_in_file("USE `{0}`;".format(old_db_name), restore_data["path_to_backup"])
            else:
                split_backup_name = restore_data["path_to_backup"].split(".")
                if split_backup_name[-1] == "sql":
                    self.make_tcp_request(self.utils["psql-path"], " -d {0} -f {1}".format(formatted_new_db_name, restore_data["path_to_backup"]))
                else:
                    self.make_tcp_request(self.utils["pg_restore-path"], " -d {0} -1 {1}".format(formatted_new_db_name, restore_data["path_to_backup"]))
        except Exception as e:
            try:
                raise Exception(e)
            finally:
                e = None
                del e

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/dbms/postgres/full.pyc
