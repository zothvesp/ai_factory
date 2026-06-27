
import json
from lib2to3.pgen2 import token
import os, apiclient
from apiclient import http
import httplib2, requests
from oauth2client import client
from sqlbak.destinations.helper.oauth import Token
from sqlbak.definitions import DESTINATIONS_NAMES, CONFIG
from sqlbak.helper import Helper
from sqlbak.logger import log_method
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import get_correct_path

class GoogleDestination:

    @log_method
    def __init__(self, params=None):
        self.params = params
        self.helper = Helper()
        self.destination_path = get_correct_path(params["DestinationPath"]).strip("/").strip("\\")
        self.destination_name = DESTINATIONS_NAMES[params["DestinationType"]]
        self.destination_id = params["DestinationId"]
        try:
            if "DestinationId" in params:
                self.Token = Token.from_destionation_id(params["DestinationId"]) if params["DestinationId"] > 0 else Token(params["AccessToken"])
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

    def connect(self):
        self.headers = {"Authorization": ("Bearer {0}".format(self.Token.Value()))}
        self.url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
        self.folder_mime_type = "application/vnd.google-apps.folder"

    def get_drive_service(self):
        self.connect()
        credentials = client.AccessTokenCredentials(self.Token.Value(), "my-user-agent/1.0")
        credentials_http = credentials.authorize(httplib2.Http())
        return apiclient.discovery.build("drive", "v3", http=credentials_http, cache_discovery=False)

    @log_method
    def does_folder_exists(self, folder_name, parent_name):
        response = self.get_drive_service().files().list(q=('trashed=False and name="{0}" and "{1}" in parents'.format(folder_name, parent_name))).execute()
        res = response.get("files")
        return {'is_exists':True if (len(res) > 0) else False, 
         'id':res[0].get("id") if (len(res) > 0) else None}

    @log_method
    def get_folder_id(self, folder_path):
        folder_id = None
        if self.helper.is_url_valid(self.destination_path):
            url_path = self.helper.get_url_path(self.destination_path)
            folder_id = self.parse_url_path_to_get_folder_id(url_path)
        else:
            for (idx, path_to) in enumerate(folder_path.replace("\\", "/").split("/")):
                folder_info = self.does_folder_exists(path_to, "root" if idx == 0 else folder_id)
                folder_id = folder_info["id"]

        if folder_id is None:
            return "root"
        return folder_id

    @log_method
    def create_destination_folder(self):
        for (idx, path_to) in enumerate(self.destination_path.replace("\\", "/").split("/")):
            folder_info = self.does_folder_exists(path_to, "root" if idx == 0 else parent_id)
            if not folder_info["is_exists"]:
                file_metadata = {'name':path_to,  'mimeType':self.folder_mime_type, 
                 'parents':[
                  "root" if idx == 0 else parent_id]}
                folder = self.get_drive_service().files().create(body=file_metadata, fields="id").execute()
                parent_id = folder["id"]
            else:
                parent_id = folder_info["id"]

        return parent_id

    @log_method
    def send_backup_to_destination(self, path_to_file, file_name):
        file_metadata = {'name':file_name, 
         'mimeType':"*/*"}
        if self.destination_path.strip() != "":
            if self.helper.is_url_valid(self.destination_path):
                url_path = self.helper.get_url_path(self.destination_path)
                folder_id = self.parse_url_path_to_get_folder_id(url_path)
                file_metadata["parents"] = [
                 folder_id]
            else:
                file_metadata["parents"] = [
                 self.create_destination_folder()]
        media = http.MediaFileUpload((path_to_file + file_name), mimetype="*/*", resumable=True)
        req = self.get_drive_service().files().create(body=file_metadata, media_body=media, fields="id")
        res = None
        t = self.Token.Value()
        while res is None:
            if t != self.Token.Value():
                req.http = client.AccessTokenCredentials(self.Token.Value(), "my-user-agent/1.0").authorize(httplib2.Http())
                t = self.Token.Value()
            (status, res) = req.next_chunk()

        return res["id"]

    @log_method
    def parse_url_path_to_get_folder_id(self, url_path):
        split_url_path = url_path.replace("\\", "/").split("/")
        return split_url_path[-1]

    @log_method
    def get_uploaded_file_size(self, file_name, outId=None):
        if outId is not None:
            return self.get_drive_service().files().get(fileId=outId, fields="size").execute()["size"]
        return [f["size"] for f in self.get_files_from_destination() if f["name"] == file_name.strip("/")][0]

    @log_method
    def get_files_from_destination(self):
        files = []
        next_page_token = None
        while True:
            folder_id = self.get_folder_id(self.destination_path)
            if next_page_token is None:
                response = self.get_drive_service().files().list(q=('trashed=False and "{0}" in parents'.format(folder_id)), fields="*").execute()
            else:
                response = self.get_drive_service().files().list(q=('trashed=False and "{0}" in parents'.format(folder_id)), pageToken=next_page_token, fields="*").execute()
            for f in response["files"]:
                files.append({'name':f["name"],  'id':f["id"],  'size':f["size"] if ("size" in f) else 0})

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return files

    @log_method
    def get_file_names_placed_at_destination(self):
        return [f["name"] for f in self.get_files_from_destination()]

    @log_method
    def get_file_id_by_name(self, file_name):
        files = [f["id"] for f in self.get_files_from_destination() if f["name"] == file_name]
        if len(files) > 0:
            return files[0]
        return

    @log_method
    def delete_file(self, file_name, outId=None):
        self.connect()
        if outId is not None:
            file_id = outId
        else:
            file_id = self.get_file_id_by_name(file_name)
        if file_id is None:
            raise DestinationFileDoesNotExist
        if not self.is_file_exist(file_name, file_id):
            raise DestinationFileDoesNotExist
        url = "https://www.googleapis.com/drive/v3/files/{0}".format(str(file_id))
        res = requests.delete(url, headers=(self.headers))
        self.helper.is_correct_response(res)

    def close_connection(self):
        pass

    def is_file_existParse error at or near `SETUP_FINALLY' instruction at offset 0

    @log_method
    def download_file(self, src, dst, outId=None):
        self.connect()
        if outId is not None:
            file_id = outId
        else:
            file_id = self.get_file_id_by_name(src)
        if file_id is None:
            raise DestinationFileDoesNotExist
        url = "https://www.googleapis.com/drive/v3/files/" + str(file_id) + "?alt=media"
        res = requests.get(url, headers=(self.headers))
        self.helper.is_correct_response(res)
        with open(dst + src, "wb") as f:
            f.write(res.content)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass
