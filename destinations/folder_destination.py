from os import remove
from os.path import getsize, exists
from sqlbak.helper import Helper
from sqlbak.logger import log_method, log_data, log_error
from sqlbak.native_command import NativeCommand
from sqlbak.definitions import CONFIG
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import get_correct_path, create_directory

class FolderDestination:

    @log_method
    def __init__(self, params=None):
        self.params = params
        self.helper = Helper()
        self.destination_path = get_correct_path(self.params["DestinationPath"])
        self.native_command = NativeCommand()

    def connect(self):
        return

    @log_method
    def send_backup_to_destination(self, path_to_backup, backup_name):
        create_directory(self.destination_path)
        self.native_command.copy_resource(path_to_backup + backup_name, self.destination_path + backup_name)

    @log_method
    def get_uploaded_file_size(self, path_to_file, outid=None):
        return getsize(self.destination_path + path_to_file)

    def close_connection(self):
        return

    @log_method
    def get_file_names_placed_at_destination(self):
        return self.helper.get_files_in_directory(self.destination_path)

    @log_method
    def delete_file(self, file_name, outId=None):
        log_data("Deleting file: {0}".format(self.destination_path + file_name))
        if not self.is_file_exist(file_name):
            log_data("File does not exist")
            raise DestinationFileDoesNotExist
        if self.destination_path == "/":
            if file_name == "":
                raise Exception("Cannot delete root directory")
        try:
            remove(self.destination_path + file_name)
        except Exception as e:
            try:
                log_error(e, "Error while deleting file")
                self.native_command.run_linux_script("rm -rf {0}".format(self.destination_path + file_name))
            finally:
                e = None
                del e

    @log_method
    def is_file_exist(self, file_name, outId=None):
        log_data("Checking if file exists: {0}".format(self.destination_path + file_name))
        return exists(self.destination_path + file_name)

    @log_method
    def download_file(self, file_name, path_to, outId=None):
        self.native_command.copy_resource(self.destination_path + file_name, path_to + file_name)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/folder_destination.pyc
