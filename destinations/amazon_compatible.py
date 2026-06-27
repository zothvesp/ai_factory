import boto3
from botocore.client import Config
from sqlbak.helper import Helper
from sqlbak.logger import log_method
from sqlbak.definitions import CONFIG, M_BIT
from boto3.s3.transfer import TransferConfig
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import create_directory, get_correct_path

class AmazonCompatibleDestination:

    @log_method
    def __init__(self, params=None):
        helper = Helper()
        self.access_key = params["AccessKey"].strip("")
        self.secret_key = params["SecretKey"].strip("")
        self.destination_path = get_correct_path(params["DestinationPath"]).lstrip("/")
        self.bucket = params["BucketName"].strip("")
        self.auth_region = params["AuthenticationRegion"].strip("")
        self.params = params
        self.connection = None

    @log_method
    def connect(self):
        endpoint_url = self.params["EndPoint"]
        if self.auth_region != "":
            self.connection = boto3.client("s3", region_name=(self.auth_region), endpoint_url=endpoint_url, aws_access_key_id=(self.access_key), aws_secret_access_key=(self.secret_key))
        elif "gra.cloud.ovh.net" in endpoint_url:
            self.connection = boto3.client("s3", region_name="GRA", endpoint_url=endpoint_url, aws_access_key_id=(self.access_key), aws_secret_access_key=(self.secret_key))
        elif "home.majicware.com" in endpoint_url:
            self.connection = boto3.client("s3", region_name="home", endpoint_url=endpoint_url, aws_access_key_id=(self.access_key), aws_secret_access_key=(self.secret_key))
        else:
            self.connection = boto3.client("s3", endpoint_url=endpoint_url, aws_access_key_id=(self.access_key), aws_secret_access_key=(self.secret_key))

    def try_get_get_file_list(self):
        self.connection.list_objects_v2(Bucket=(self.bucket))

    @log_method
    def send_backup_to_destination(self, path_to_backup, backup_name):
        config = TransferConfig(multipart_threshold=(M_BIT * 25), max_concurrency=10, multipart_chunksize=(M_BIT * 25),
          use_threads=(self.params["ConcurrentUpload"]))
        self.connection.upload_file((path_to_backup + backup_name), (self.bucket), (self.destination_path + backup_name), Config=config)

    @log_method
    def get_file_names_placed_at_destination(self):
        files = []
        next_token = None
        while True:
            if not next_token:
                res = self.connection.list_objects_v2(Bucket=(self.bucket), MaxKeys=128)
            else:
                res = self.connection.list_objects_v2(Bucket=(self.bucket), ContinuationToken=next_token, MaxKeys=128)
            if "Contents" in res:
                for f in res["Contents"]:
                    files.append(f["Key"])

                if "IsTruncated" in res:
                    if not res["IsTruncated"]:
                        break
                    if "NextContinuationToken" in res:
                        next_token = res["NextContinuationToken"]

        return files

    @log_method
    def delete_file(self, file_name, outId=None):
        if not self.is_file_exist(file_name):
            raise DestinationFileDoesNotExist
        self.connection.delete_object(Bucket=(self.bucket), Key=(self.destination_path + file_name.strip("/")))

    def close_connection(self):
        pass

    @log_method
    def get_uploaded_file_size(self, file_name, outid=None):
        obj = self.connection.get_object(Bucket=(self.bucket), Key=(self.destination_path + file_name.strip("/")))
        return obj["ContentLength"]

    @log_method
    def is_file_exist(self, file_name, outid=None):
        for f in self.get_file_names_placed_at_destination():
            if f == self.destination_path + file_name.strip("/"):
                return True
            return False

    @log_method
    def download_file(self, src, dst, outId=None):
        self.connection.download_file(self.bucket, self.destination_path + src, dst + src)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.connect()
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/amazon_compatible.pyc
