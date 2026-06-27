import json, requests
from sqlbak.definitions import DESTINATIONS_NAMES, CONFIG, TIMEOUT, K_BIT
from sqlbak.helper import Helper
from sqlbak.native_command import NativeCommand
from sqlbak.logger import log_method, log_only_exception
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import get_correct_path
from sqlbak.destinations.helper.oauth import Token

class OneDriveDestination:

    @log_method
    def __init__(self, params=None):
        self.params = params
        self.helper = Helper()
        self.native_command = NativeCommand()
        self.url = "https://graph.microsoft.com/v1.0"
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
            self.destination_path = get_correct_path(params["DestinationPath"]).strip("/")
            self.destination_name = DESTINATIONS_NAMES[params["DestinationType"]]
            self.cm = APP_OUTPUT[CONFIG["LOCALE"]]

    def get_header(self):
        return {'Authorization':("Bearer {0}".format)(self.Token.Value()), 
         'Accept':"application/json, application/xml, text/json, text/x-json, text/javascript, text/xml", 
         'Content-Type':"application/json"}

    def connect(self):
        return

    @log_method
    def get_item(self, item):
        try:
            res = requests.get((self.url + "/me/drive/root:/{}".format(item.strip("/"))), headers=(self.get_header()), timeout=TIMEOUT)
            self.helper.is_correct_response(res)
            return res.json()
        except:
            except Exception:
            return

    @log_method
    def create_folder_and_return_id(self):
        path_list = []
        for idx, path_to in enumerate(self.destination_path.split("/")):
            path_list.append(path_to)
            item_data = self.get_item(path_to if idx == 0 else "/".join(path_list))
            if item_data is not None:
                item_id = item_data["id"]
            else:
                item_id = self.create_folder(path_to, "root" if idx == 0 else item_id)
        else:
            return item_id

    @log_method
    def create_folder(self, path_to, parent_path):
        url_params = "/me/drive/items/{0}/children".format(parent_path)
        data = {'name':path_to, 
         'folder':{},  '@microsoft.graph.conflictBehavior':"rename"}
        res = requests.post((self.url + url_params), headers=(self.get_header()), data=(json.dumps(data)))
        self.helper.is_correct_response(res)
        return res.json()["id"]

    @log_method
    def send_backup_to_destination(self, path_to_backup, backup_name):
        index = 0
        folder_id = self.get_folder_id()
        session = self.create_upload_session(folder_id, backup_name)
        full_file_size = self.helper.get_resource_size(path_to_backup + backup_name)
        file_in_bytes = open(path_to_backup + backup_name, "rb")
        for chunk in self.helper.read_file_by_chunks_test(file_in_bytes, 320 * K_BIT):
            offset = index + len(chunk) - 1
            upload_headers = {'Content-length':str(len(chunk)), 
             'Content-Range':("bytes {0}-{1}/{2}".format)(index, offset, full_file_size)}
            index = offset + 1
            self.send_data(session["uploadUrl"], upload_headers, chunk)

    @log_method
    def create_upload_session(self, folder_id, file_name):
        url_params = "/me/drive/items/{}:/{}:/createUploadSession".format(folder_id, file_name)
        data = {'fileSystemInfo':{"@odata.type": "microsoft.graph.fileSystemInfo"}, 
         'name':file_name}
        res = requests.post((self.url + url_params), headers=(self.get_header()), data=(json.dumps(data)))
        self.helper.is_correct_response(res)
        upload_session = res.json()
        if "uploadUrl" not in upload_session:
            raise Exception(self.cm["FAILED_URL"])
        return upload_session

    @log_method
    def get_uploaded_file_size(self, file_name, outid=None):
        path_to_resource = self.destination_path + "/" + file_name
        item_data = self.get_item(path_to_resource)
        if item_data is not None:
            return item_data["size"]
        raise Exception(self.cm["FAILED_GET_ONE_DRIVE_ITEM"].format(path_to_resource))

    @log_method
    def get_file_names_placed_at_destination(self):
        url_params = "/me/drive/root:/{}:/children".format(self.destination_path)
        res = requests.get((self.url + url_params), headers=(self.get_header()), timeout=TIMEOUT)
        self.helper.is_correct_response(res)
        data = res.json()
        return [d["name"] for d in data["value"]]

    @log_method
    def delete_file(self, file_name=None, outId=None):
        if not self.is_file_exist(file_name):
            raise DestinationFileDoesNotExist
        folder_id = self.get_folder_id()
        self.delete_file_at_destination(folder_id, file_name)

    @log_method
    def delete_file_at_destination(self, folder_id, file_name):
        url_params = "/me/drive/items/{}:/{}".format(folder_id, file_name.strip("/"))
        res = requests.delete((self.url + url_params), headers=(self.get_header()), timeout=20)
        self.helper.is_correct_response(res)

    def close_connection(self):
        return

    @log_method
    def is_file_exist(self, file_name, outid=None):
        destination = self.destination_path + "/" if self.destination_path != "" else ""
        item_data = self.get_item(destination + file_name)
        if item_data is None:
            return False
        return True

    @log_method
    def download_file(self, src, dst, outId=None):
        item_id = self.get_item_id(src)
        file_content = self.download_file_content(item_id)
        self.save_download_file(dst + src, file_content)

    @log_method
    def get_item_id(self, path_to_file):
        root_dir = self.destination_path + "/" if self.destination_path != "" else ""
        item_data = self.get_item(root_dir + path_to_file)
        if item_data is None:
            raise Exception(self.cm["FAILED_GET_ONE_DRIVE_ITEM"].format(root_dir + path_to_file))
        return item_data["id"]

    @log_method
    def download_file_content(self, item_id):
        url_params = "/me/drive/items/{0}/content".format(item_id)
        res = requests.get((self.url + url_params), headers=(self.get_header()))
        self.helper.is_correct_response(res)
        return res.content

    @log_method
    def save_download_file(self, save_to_file, file_content):
        with open(save_to_file, "wb") as f:
            f.write(file_content)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.upload_file(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

    @log_method
    def upload_file(self, path_to_file, file_name):
        folder_id = self.get_folder_id()
        file_data = self.get_file_data(path_to_file + file_name)
        url_params = "/me/drive/items/{0}:/{1}:/content".format(folder_id, file_name)
        self.send_data(self.url + url_params, self.get_header(), file_data)

    @log_method
    def get_folder_id(self):
        folder_id = None
        if self.destination_path != "":
            folder_id = self.create_folder_and_return_id()
        if folder_id is None:
            return "root"
        return folder_id

    @log_method
    def get_file_data(self, path_to_file):
        file_data = None
        with open(path_to_file, "rb") as f:
            file_data = f.read()
        return file_data

    @log_only_exception
    def send_data(self, url, headers, file_data):
        res = requests.put(url, headers=headers, data=file_data)
        self.helper.is_correct_response(res)
        return res

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/one_drive_destination.pyc
