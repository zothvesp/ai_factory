from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode, UploadSessionCursor, CommitInfo
from sqlbak.destinations.helper.oauth import Token
from sqlbak.helper import Helper
from sqlbak.logger import log_method, log_only_exception
from sqlbak.definitions import CONFIG, M_BIT
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import get_correct_path

class DropBoxDestination:

    @log_method
    def __init__(self, params=None):
        self.params = params
        self.helper = Helper()
        try:
            self.Token = Token.from_destionation_id(params["DestinationId"]) if ("DestinationId" in params and params["DestinationId"] > 0) else (Token(params["AccessToken"]))
            if "AccessToken" in params:
                self.Token.Value()
        except Exception as e:
            try:
                if "PSB:0034" in str(e) and "AccessToken" in params:
                    self.Token = Token(params["AccessToken"])
                else:
                    raise e
            finally:
                e = None
                del e

        else:
            self.is_connected = False
            temp_path = get_correct_path(params["DestinationPath"])
            self.destination_path = "/" if temp_path == "" else temp_path
            self.cm = APP_OUTPUT[CONFIG["LOCALE"]]
            self.dbx = None

    def get_dbx(self):
        if self.dbx is None:
            self.dbx = Dropbox((self.Token.Value()), timeout=900)
        return self.dbx

    @log_method
    def connect(self):
        access_token = self.Token.Value()
        if self.Token.Value() is None or len(access_token) == 0:
            raise Exception(self.cm["FAILED_CONNECT_DROPBOX"])

    @log_method
    def send_backup_to_destination(self, path_to_backup, file_name):
        try:
            chunk_size = 4 * M_BIT
            file_size = self.helper.get_resource_size(path_to_backup + file_name)
            with open(path_to_backup + file_name, "rb") as f:
                if file_size <= chunk_size:
                    self.get_dbx().files_upload((f.read()), (self.destination_path + file_name), mode=(WriteMode("overwrite")))
                else:
                    self.upload_large_file(f, chunk_size, file_name, file_size)
        except Exception as e:
            try:
                raise Exception(self.cm["FAILED_UPLOAD_DROPBOX"].format(str(e)))
            finally:
                e = None
                del e

    @log_method
    def upload_large_file(self, f, chunk_size, file_name, file_size):
        upload_session_start_result = self.get_dbx().files_upload_session_start(f.read(chunk_size))
        cursor = UploadSessionCursor(session_id=(upload_session_start_result.session_id), offset=(f.tell()))
        commit = CommitInfo(path=(self.destination_path + file_name), mode=(WriteMode("overwrite")))
        while f.tell() < file_size:
            if file_size - f.tell() <= chunk_size:
                self.get_dbx().files_upload_session_finish(f.read(chunk_size), cursor, commit)
            else:
                self.get_dbx()._oauth2_access_token = self.Token.Value()
                self.get_dbx().files_upload_session_append_v2(f.read(chunk_size), cursor)
                cursor.offset = f.tell()

    @log_method
    def get_uploaded_file_size(self, file_name, outid=None):
        files = [f.size for f in self.get_files_at_destination() if f.name == file_name]
        if len(files) > 0:
            return files[0]
        return 0

    @log_method
    def get_files_at_destination(self):
        res = self.get_dbx().files_list_folder("" if self.destination_path == "/" else self.destination_path)
        files = self.handle_files([], res.entries)
        while res.has_more:
            res = self.get_dbx().files_list_folder_continue(res.cursor)
            files = self.handle_files(files, res.entries)

        return files

    @log_only_exception
    def handle_files(self, files, entries):
        for r in entries:
            files.append(r)
        else:
            return files

    @log_method
    def get_file_names_placed_at_destination(self):
        return [f.name for f in self.get_files_at_destination()]

    @log_method
    def delete_file(self, file_name, outId=None):
        self.get_dbx()._oauth2_access_token = self.Token.Value()
        if not self.is_file_exist(file_name):
            raise DestinationFileDoesNotExist
        self.get_dbx().files_delete_v2(self.destination_path + file_name)

    def close_connection(self):
        return

    @log_method
    def is_file_exist(self, file_name, outid=None):
        for f in self.get_file_names_placed_at_destination():
            if f == file_name:
                return                 return True
            return False

    @log_method
    def download_file(self, src, dst, outId=None):
        self.get_dbx().files_download_to_file(dst + src, self.destination_path + src)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.connect()
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/drop_box_destination.pyc
