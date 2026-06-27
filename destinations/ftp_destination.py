from ftplib import FTP, FTP_TLS
from logging import Logger
import os, io
from paramiko import AutoAddPolicy, SSHClient, RSAKey
from sqlbak.definitions import FTP_PROTOCOLS, CONFIG
from sqlbak.helper import Helper
from sqlbak.logger import log_method, log_data
from sqlbak.app_output import APP_OUTPUT
from sqlbak.native_command import NativeCommand
from sqlbak.putty import ppkraw_to_openssh
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import get_correct_path

class FTPDestination:

    @log_method
    def __init__(self, params=None):
        self.params = params
        self.protocol = self.get_ftp_protocol()
        self.helper = Helper()
        self.destination_path = get_correct_path(params["DestinationPath"])
        self.connection = None
        self.native_command = NativeCommand()

    @log_method
    def get_ftp_protocol(self):
        if self.params["DestinationFtpProtocol"] == FTP_PROTOCOLS["FTP"]:
            if self.params["SslMode"] is not None and self.params["SslMode"] == "Implicit":
                protocol = FTP_PROTOCOLS["FTP_IMPLICIT"]
        elif self.params["SslMode"] is not None:
            if self.params["SslMode"] == "Explicit":
                protocol = FTP_PROTOCOLS["FTP_EXPLICIT"]
            else:
                protocol = FTP_PROTOCOLS["FTP"]
        else:
            protocol = FTP_PROTOCOLS["SFTP"]
        return protocol

    @log_method
    def __del__(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                try:
                    log_data("Error while closing connection: {0}".format(str(e)))
                finally:
                    e = None
                    del e

    @log_method
    def ftps_connection(self):
        self.connection = FTP_TLS(self.params["DestinationHost"], self.params["DestinationUser"], self.params["DestinationPassword"])
        self.connection.prot_p()

    @log_method
    def ftp_connect(self):
        self.connection = FTP()
        self.get_ftp_connection()
        self.get_ftp_login()

    @log_method
    def get_ftp_connection(self):
        log_data("Host: {0}. Port: {1}. ".format(self.params["DestinationHost"], self.params["DestinationPort"]))
        self.connection.connect(self.params["DestinationHost"], int(self.params["DestinationPort"]))

    @log_method
    def get_ftp_login(self):
        self.connection.login(self.params["DestinationUser"], self.params["DestinationPassword"])

    @log_method
    def sftp_connect(self):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if self.params["SFtpAuthenticationMethod"] == "PublicKey":
            self.check_fingerprints()
            ssh_key = ppkraw_to_openssh(self.params["SshPrivateKey"])
            ssh.connect((self.params["DestinationHost"]), port=(int(self.params["DestinationPort"])), username=(self.params["DestinationUser"]), pkey=(RSAKey.from_private_key(io.StringIO(ssh_key))))
        else:
            ssh.connect((self.params["DestinationHost"]), port=(int(self.params["DestinationPort"])), username=(self.params["DestinationUser"]), password=(self.params["DestinationPassword"]))
        self.connection = ssh.open_sftp()

    @log_method
    def check_fingerprints(self):
        if self.params["VerifyServerFingerprint"]:
            if self.params["ServerFingerprint"] != "":
                fp = self.get_fingerprint_from_server()
                parsed_finger_print = self.parse_finger_print(fp)
                if "".join(parsed_finger_print[1[:None]]) != self.params["ServerFingerprint"]:
                    raise Exception(APP_OUTPUT[CONFIG["LOCALE"]]["FAILED_FINGERPRINT"])

    @log_method
    def get_fingerprint_from_server(self):
        path_to_tmp_ssh_key = "/tmp/ssh_key"
        cmd = "ssh-keyscan -t rsa -p {1} {0} > {2} 2> /dev/null".format(self.params["DestinationHost"], int(self.params["DestinationPort"]), path_to_tmp_ssh_key)
        self.native_command.run_linux_script(cmd)
        cmd = "ssh-keygen -E md5 -lf {0}".format(path_to_tmp_ssh_key)
        res = self.native_command.run_linux_script(cmd)
        self.helper.remove_file_or_dir([path_to_tmp_ssh_key])
        return res

    @log_method
    def parse_finger_print(self, tmp_fingerprint):
        split_res = tmp_fingerprint.split()
        return split_res[1].split(":")

    @log_method
    def connect(self):
        if self.protocol == FTP_PROTOCOLS["FTP"]:
            self.ftp_connect()
        else:
            if self.protocol == FTP_PROTOCOLS["SFTP"]:
                self.sftp_connect()
            else:
                self.ftps_connection()

    @log_method
    def send_backup_to_ftp(self, path_to_backup, backup_name):
        if self.destination_path != "":
            self.create_ftp_directory_if_not_exists(self.destination_path)
        with open(path_to_backup + backup_name, "rb") as f:
            self.connection.storbinary("STOR " + self.destination_path + backup_name, f, 1024)

    @log_method
    def send_backup_to_sftp(self, path_to_backup, backup_name):
        tmp_dir = self.create_dir_at_sftp()
        self.connection.put(path_to_backup + backup_name, tmp_dir + backup_name)

    @log_method
    def create_dir_at_sftp(self):
        destination_path = self.destination_path.strip("/")
        tmp_dir = []
        if destination_path != "":
            split_dir = destination_path.split("/")
            if len(split_dir) > 0:
                for idx, d in enumerate(split_dir):
                    if d != "":
                        if idx == 0:
                            tmp_dir.append("/" + d)
                            self.connection.chdir("/")
                        else:
                            tmp_dir.append(d)
                        list_dir = self.connection.listdir()
                        if d not in list_dir:
                            self.connection.mkdir("/".join(tmp_dir))
                        self.connection.chdir("/".join(tmp_dir))

        return "/".join(tmp_dir) + "/"

    @log_method
    def create_ftp_directory_if_not_exists(self, directory):
        directory = directory.strip("/")
        if "/" in directory:
            for path in directory.split("/"):
                if path in self.connection.nlst():
                    self.connection.cwd(path)
                else:
                    self.connection.mkd(path)

        else:
            ftp_directories = self.connection.nlst()
            if directory not in ftp_directories:
                self.connection.mkd(directory)

    @log_method
    def send_backup_to_destination(self, path_to_backup, compressed_backup_name):
        if self.protocol == FTP_PROTOCOLS["SFTP"]:
            self.send_backup_to_sftp(path_to_backup, compressed_backup_name)
        else:
            self.send_backup_to_ftp(path_to_backup, compressed_backup_name)

    @log_method
    def get_file_size_from_ftp(self, path_to_file):
        arr = path_to_file.split(".")
        if len(arr) > 1:
            extension = path_to_file[-1]
            if extension != "txt":
                self.connection.sendcmd("TYPE I")
            return self.connection.size(self.destination_path + path_to_file)

    @log_method
    def get_file_size_from_sftp(self, path_to_file):
        res = self.connection.stat(self.destination_path + path_to_file)
        return int(res.st_size)

    @log_method
    def get_uploaded_file_size(self, path_to_file, outid=None):
        if self.protocol == FTP_PROTOCOLS["SFTP"]:
            size = self.get_file_size_from_sftp(path_to_file)
        else:
            size = self.get_file_size_from_ftp(path_to_file)
        return size

    @log_method
    def get_backup_files_from_ftp(self):
        self.connection.cwd(self.destination_path)
        return [f for f in self.connection.nlst()]

    @log_method
    def get_backup_files_from_sftp(self):
        destination = "/" if self.destination_path == "" else self.destination_path
        return self.connection.listdir(destination)

    @log_method
    def get_file_names_placed_at_destination(self):
        if self.protocol == FTP_PROTOCOLS["SFTP"]:
            return self.get_backup_files_from_sftp()
        return self.get_backup_files_from_ftp()

    @log_method
    def delete_file(self, file_name, outId=None):
        if not self.is_file_exist(file_name):
            raise DestinationFileDoesNotExist
        elif self.protocol == FTP_PROTOCOLS["SFTP"]:
            self.connection.remove(self.destination_path + file_name)
        else:
            self.connection.delete(self.destination_path + file_name)

    def close_connection(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                try:
                    log_data("Error while closing connection: {0}".format(str(e)))
                finally:
                    e = None
                    del e

    @log_method
    def is_file_exist(self, file_name, outId=None):
        for f in self.get_file_names_placed_at_destination():
            if f == file_name:
                return                 return True
            return False

    @log_method
    def download_file(self, src, dst, outId=None):
        if self.protocol == FTP_PROTOCOLS["SFTP"]:
            self.connection.get(self.destination_path + src, dst + src)
        else:
            with open(dst + src, "wb") as f:
                self.connection.retrbinary("RETR {0}".format(self.destination_path + src), f.write)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.connect()
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

    @log_method
    def test_sftp_destination(self):
        fp = self.get_fingerprint_from_server()
        parsed_finger_print = self.parse_finger_print(fp)
        return ":".join(parsed_finger_print[1[:None]])

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/ftp_destination.pyc
