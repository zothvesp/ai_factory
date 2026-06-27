
import os, subprocess, re, json
from sqlbak.local_db import local_db_instanse
from sqlbak.process_managment.helper import get_env_for_invoke_system_command
from sqlbak.logger import log_error, log_method, log_data
from sqlbak.definitions import CONFIG, COMPRESSION_ENGINE_7Z, MSSQL_LOGIN_TIMEOUT
from sqlbak.dbms.postgres.psql_params import PSQL_PARAMETERS
from sqlbak.app_output import APP_OUTPUT
from sqlbak.helper import Helper, helper_instanse
from sqlbak.helpers.strings import is_empty

class NativeCommand:

    def __init__(self):
        self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    @log_method
    def try_run_linux_scriptParse error at or near `SETUP_FINALLY' instruction at offset 0

    def run_linux_script_as_fileParse error at or near `LOAD_CONST' instruction at offset 0

    @log_method
    def run_linux_script(self, command_args):
        try:
            log_data(command_args)
            completed = subprocess.run(command_args, check=True, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), env=(get_env_for_invoke_system_command()))
        except subprocess.CalledProcessError as err:
            try:
                raise Exception(str(err.stderr.decode"utf-8"))
            finally:
                err = None
                del err

        except Exception as err:
            try:
                raise err
            finally:
                err = None
                del err

        else:
            result = completed.stdout.decode
            log_data(result)
            return str(completed.stdout.decode)

    @log_method
    def run_linux_script_with_password(self, command_args, passwords=[]):
        try:
            log_data(self.replace_passwords_in_params_arrcommand_argspasswords)
            completed = subprocess.run(command_args, check=True, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), env=(get_env_for_invoke_system_command()))
        except subprocess.CalledProcessError as err:
            try:
                error = str(err.stderr.decode"utf-8")
                error = self.replace_passwordserrorpasswords
                log_data(error)
                raise Exception(error)
            finally:
                err = None
                del err

        except Exception as err:
            try:
                error = str(err)
                error = self.replace_passwordserrorpasswords
                log_data(error)
                raise Exception(error)
            finally:
                err = None
                del err

        else:
            result = str(completed.stdout.decode)
            log_data(result)
            return result

    @log_method
    def replace_passwords_in_params_arr(self, params_arr, passwords):
        return self.replace_passwordsparams_arrpasswords

    def replace_passwords(self, log_string, passwords):
        for p in passwords:
            log_string = log_string.replacep"my_pass"
        else:
            return log_string

    @log_method
    def join_split_resource(self, source_dir, destination_dir):
        """

        :param source_dir: str
        :param destination_dir: str
        :return:
        """
        cmd = "cat {0}* > {1}".formatsource_dirdestination_dir
        self.run_linux_scriptcmd

    @log_method
    def compress_backup(self, engine, level, password, is_encrypted, dst_dir, source_dir, backup_name, path_to_backup, command_line_params):
        """

        :param engine:
        :param level:
        :param password:
        :param is_encrypted:
        :param dst_dir:
        :param source_dir:
        :return:
        """
        compress_method = self.compress_backup_by_7_zip if engine == COMPRESSION_ENGINE_7Z else self.compress_backup_by_zip
        return compress_method(level, password, is_encrypted, dst_dir, source_dir, backup_name, path_to_backup, command_line_params)

    @log_method
    def compress_backup_by_zip(self, compression_level, password, is_encrypted, dst_dir, source_dir, backup_name, path_to_backup, command_line_params=None):
        """

        :param compression_level:
        :param password:
        :param is_encrypted:
        :param dst_dir:
        :param source_dir:
        :param path_to_backup:
        :return:
        """
        if not os.path.existssource_dir:
            raise Exception(self.cm["FILE_NOT_EXISTS"].formatstr(source_dir))
        is_backup_dir = os.path.isdirsource_dir
        password = password.replace"'""'\\''"
        cmd = "{5} zip -r {0} {1} -q {2} '{3}' '{4}'".format(compression_level, "-P '{0}'".formatpassword if is_encrypted else "", "" if is_backup_dir else "-j", dst_dir, backup_name + "/" if is_backup_dir else source_dir, "cd {0};".formatpath_to_backup if is_backup_dir else "")
        self.run_linux_script_with_passwordcmd([password] if is_encrypted else [])
        return cmd

    @log_method
    def decompress_by_7zip(self, source_dir, destination_dir, password):
        """

        :param source_dir: str
        :param destination_dir: str
        :param password: str
        :return:
        """
        cmd = '7z x \'{0}\' -o\'{1}\' "-p{2}" > /dev/null'.format(source_dir, destination_dir, password)
        self.run_linux_script_with_passwordcmd[password]

    @log_method
    def decompress_by_unzip(self, source_dir, destination_dir, password):
        if is_empty(password):
            cmd = 'unzip \'{0}\' -d "{1}" '.formatsource_dirdestination_dir
        else:
            cmd = 'unzip -P \'{2}\' -d "{1}" \'{0}\' '.format(source_dir, destination_dir, password)
        self.run_linux_script_with_passwordcmd[password]

    @log_method
    def compress_backup_by_7_zip(self, compression_level, password, is_encrypted, dst_file, source_dir, backup_name, path_to_backup, command_line_params):
        """

        :param compression_level:
        :param password:
        :param is_encrypted:
        :param dest_dir:
        :param source_dir:
        :param path_to_backup:
        :return:
        """
        compression_level_param = compression_level.split"="[0]
        params = self.parse_compression_level_param(command_line_params, compression_level_param, compression_level)
        cmd = "7z a {0} {1} '{2}' '{3}' > /dev/null".format(params, '-p"{0}"'.formatpassword if is_encrypted else "", dst_file, source_dir)
        self.run_linux_script_with_passwordcmd([password] if is_encrypted else [])
        return cmd

    @log_method
    def check_installed_utilParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def make_tcp_request_to_sqlpackage_export(self, params):
        host, user, password, command, request = params
        query = ' /action:Export  /SourceServerName:"{0}" /SourceUser:"{1}" /SourcePassword:"{2}" '.format(host, user, password)
        cmd = command + query + request
        result = self.run_linux_scriptcmd
        return result

    @log_method
    def make_tcp_request_to_sqlpackage_import(self, params):
        host, user, password, command, request = params
        query = ' /action:Import  /TargetServerName:"{0}" /TargetUser:"{1}" /TargetPassword:"{2}" '.format(host, user, password)
        cmd = command + query + request
        result = self.run_linux_scriptcmd
        return result

    @log_method
    def parse_compression_level_param(self, command_line_params, compression_level_param, compression_level):
        params = []
        is_compression_level_changed = False
        if command_line_params:
            for p in command_line_params.split:
                if "=" in p and p.split"="[0] == compression_level_param:
                    params.appendp
                    is_compression_level_changed = True
                else:
                    params.appendp

        else:
            params.appendcompression_level
        if not is_compression_level_changed:
            params.appendcompression_level
        return " ".joinparams

    @log_method
    def make_tcp_request_to_mssql(self, params):
        host, user, port, password, command, request, use_ssh, server = params
        request_params = ' -S "{0}" -U "{1}" -P \'{2}\' -l {3} -C -d master '.format(host + "," + str(port) if port is not None else host, user, password, MSSQL_LOGIN_TIMEOUT)
        cmd = command + request_params + request
        result = self.run_linux_script_with_passwordcmd[password]
        if bool(use_ssh):
            if server is not None:
                server.stop
        return result

    @log_method
    def make_tcp_request_to_mysql(self, params, password_in_env):
        host, user, port, password, command, request, use_ssh, server = params
        if password_in_env:
            if password:
                os.environ["MYSQL_PWD"] = password
        elif password:
            request_params = ' -h "{0}" -u "{1}" -P "{2}" -p"{3}" '.format(host, user, port, password.replace"$""\\$")
        else:
            request_params = ' -h "{0}" -u "{1}" -P "{2}" '.format(host, user, port)
        command_args = command + request_params + request
        try:
            result = self.run_linux_script_with_passwordcommand_args([password] if password else [])
        finally:
            if bool(use_ssh):
                if server is not None:
                    server.stop

        return result

    @log_method
    def change_string_by_sed(self, pattern):
        cmd = "sed {0}".formatstr(pattern)
        self.run_linux_scriptcmd

    @log_method
    def remove_line_in_file(self, lines, path_to_file):
        cmd = "-i '/{0}/d' {1}".formatlinespath_to_file
        self.change_string_by_sedcmd

    @log_method
    def add_text_to_beginning_file(self, text, path_to_file):
        """

        :param text:
        :param path_to_file:
        :return:
        """
        cmd = "-i '1s/^/{0}/' {1}".formattextpath_to_file
        self.change_string_by_sedcmd

    @log_method
    def replace_substring_in_file(self, string_in, string_out, path_to_file):
        """

        :param string_in:
        :param string_out:
        :param path_to_file:
        :return:
        """
        cmd = "-i 's/^{0}/{1}/gi' {2}".format(string_in, string_out, path_to_file)
        self.change_string_by_sedcmd

    @log_method
    def cut_substring_in_file(self, substring, path_to_file):
        """

        :param substring:
        :param path_to_file:
        :return:
        """
        cmd = "-i '/^{0}/d' {1}".formatsubstringpath_to_file
        self.change_string_by_sedcmd

    @log_method
    def make_tcp_request_to_postgresql(self, params):
        """

        :param params:
        :return:
        """
        host, user, port, password, command, request, use_ssh, server = params
        request_params = ' -h {0} -U "{1}" -p {2} '.format(host, user, port)
        command_args = command + request_params + request
        if user == "postgres":
            if (password or Helper().is_local_host)host:
                result = self.run_linux_script'su - postgres -c "{0} -U {2} -p {3} {1} "'.format(command, request, user, port)
            else:
                result = self.run_linux_script'su - postgres -c "{0} -h {3} -U {2} -p {4} {1} "'.format(command, request, user, host, port)
        else:
            if password:
                result = self.run_linux_script_with_password'PGPASSWORD="{0}" {1}'.formatpasswordcommand_args[password]
            else:
                result = self.run_linux_scriptcommand_args
        if bool(use_ssh):
            if server is not None:
                server.stop
        return result

    @log_method
    def get_allowed_psql_params(self, params):
        psql_version = self.get_psql_versionparams
        psql_params = self.get_psql_parameters_by_versionpsql_version
        return psql_params

    @log_method
    def get_psql_version(self, params):
        host, user, port, password, command, request, use_ssh, server = params
        result = self.run_linux_script_with_password(command + request)([password] if password else [])
        return self.parse_psql_versionresult

    @log_method
    def parse_psql_versionParse error at or near `LOAD_CONST' instruction at offset 0

    @log_method
    def get_psql_parameters_by_version(self, version):
        if version is None:
            return []
            if "." in version:
                split_version = version.split"."
                if int(split_version[0]) > 9:
                    version = str(split_version[0])
        else:
            version = str(split_version[0]) + "." + str(split_version[1])
        if version in PSQL_PARAMETERS:
            return PSQL_PARAMETERS[str(version)]
        last = [x for x in PSQL_PARAMETERS][-1]
        return PSQL_PARAMETERS[last]

    @log_method
    def split_resource(self, max_file_size, source_path, destination_path):
        """

        :param max_file_size:
        :param source_path:
        :param destination_path:
        :return:
        """
        cmd = "split -d -b {0} {1} {2}".format(max_file_size, source_path, destination_path)
        self.run_linux_scriptcmd

    @log_method
    def copy_resource(self, src, dst):
        cmd = "cp -rf '{0}' '{1}'".formatstr(src)str(dst)
        self.run_linux_scriptcmd

    @log_method
    def get_debian_arch(self):
        try:
            result = self.run_linux_script"dpkg --print-architecture".strip"\n"
        except Exception as e:
            try:
                result = "amd64"
                log_error(e, "Can't get server architecture.")
            finally:
                e = None
                del e

        else:
            return result

    @log_method
    def get_distro_os_and_versionParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def install_deb_package(self):
        n = os.fork
        if n == 0:
            os.system'su - root -c "dpkg -i {0}"'.formatCONFIG["PATH_TO_PACKAGE"]

    @log_method
    def install_rpm_package(self):
        self.run_linux_script'su - root -c "rpm -U -p {0}" && service sqlbak restart'.formatCONFIG["PATH_TO_PACKAGE"]

    @log_method
    def restart_sqlbak_service(self):
        n = os.fork
        if n == 0:
            os.system'su - root -c "systemctl restart sqlbak.service"'

    @log_method
    def stop_sqlbak_service(self):
        n = os.fork
        if n == 0:
            os.system'su - root -c "systemctl stop sqlbak.service"'

    @log_method
    def remove_all_cron_tasks(self):
        helper = Helper()
        if not helper.is_app_run_in_docker_container:
            self.run_linux_script"(crontab -l | grep -v 'sqlbak -rjs -ji')  | crontab"

    @log_method
    def remove_auto_increment_from_dump(self, path_to_file):
        cmd = "-i 's/ AUTO_INCREMENT=[0-9]*//gi' {0}".formatpath_to_file
        self.change_string_by_sedcmd

    @log_method
    def restart_mysql_service(self):
        n = os.fork
        if n == 0:
            return os.system'su - root -c "systemctl restart mysql"'

    @log_method
    def stop_mysql_service(self):
        return os.system'su - root -c "systemctl stop mysql"'

    @log_method
    def start_mysql_service(self):
        return os.system'su - root -c "systemctl start mysql"'

    @log_method
    def move_resource(self, src, dst):
        cmd = "mv {0} {1}".formatstr(src)str(dst)
        return self.run_linux_scriptcmd

    @log_method
    def set_ownership_to_dst_resource_as_src(self, src, dst):
        cmd = "mv {0} {1}".formatstr(src)str(dst)
        return self.run_linux_scriptcmd

    @log_method
    def set_ownership_to_dst_resource_as_src(self, src, dst):
        cmd = "chown --preserve-root --no-dereference --reference={0} {1}".formatstr(src)str(dst)
        return self.run_linux_scriptcmd

    @log_method
    def set_ownership_to_dst_resource(self, user, dst):
        cmd = "chown --preserve-root --no-dereference {0} {1}".formatstr(user)str(dst)
        return self.run_linux_scriptcmd

    @log_method
    def set_permissions_to_dst_resource_as_src(self, src, dst):
        cmd = "chmod --preserve-root --reference={0} {1}".formatstr(src)str(dst)
        return self.run_linux_scriptcmd

    @log_method
    def make_directory(self, path_to_dir):
        cmd = "mkdir {1}".formatstr(path_to_dir)
        return self.run_linux_scriptcmd

    @log_method
    def make_tcp_request_to_mongo(self, params):
        host, user, port, password, command, request, use_ssh, server = params
        if user and password:
            request_params = " --host '{0}' --port '{1}' --username '{2}' --password '{3}' ".format(host, port, user, password)
        else:
            if user:
                request_params = " --host '{0}' --port '{1}' --username '{2}' ".format(host, port, user)
            else:
                request_params = " --host '{0}' --port '{1}' ".formathostport
        cmd = command + request_params + request
        result = self.run_linux_script_with_passwordcmd([password] if password else [])
        if bool(use_ssh):
            if server is not None:
                server.stop
        return result


native_command_instanse = NativeCommand()
