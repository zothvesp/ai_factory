from azure.storage.blob import BlockBlobService, BlobBlock
from sqlbak.definitions import DESTINATIONS_NAMES, CONFIG, M_BIT, TIMEOUT
from sqlbak.helper import Helper
from sqlbak.logger import log_method
from sqlbak.app_output import APP_OUTPUT
from sqlbak.exceptions import DestinationFileDoesNotExist
from sqlbak.helpers.temporary_directory import create_directory, get_correct_path

class AzureDestination:

    @log_method
    def __init__(self, params=None):
        self.helper = Helper()
        self.params = params
        self.blob_service = None
        self.base_blob_service = None
        self.destination_path = get_correct_path(params["DestinationPath"]).lstrip("/")
        self.destination_name = DESTINATIONS_NAMES[params["DestinationType"]]

    @log_method
    def connect(self):
        self.blob_service = BlockBlobService(account_name=(self.params["AccountName"]), account_key=(self.params["AccountKey"]))
        self.blob_service.create_container(self.params["ContainerName"])

    @log_method
    def send_backup_to_destination(self, path_to_backup, compressed_backup_name):
        blob_name = self.destination_path + compressed_backup_name
        block_size = 4 * M_BIT
        blocks = []
        error = None
        with open(path_to_backup + compressed_backup_name, "rb") as f:
            file_bytes = f.read(block_size)
            attempt = 1
            while len(file_bytes) > 0:
                if attempt < 5:
                    try:
                        block_id = self.helper.get_random_name(32)
                        self.blob_service.put_block((self.params["ContainerName"]), blob_name, file_bytes, block_id, timeout=TIMEOUT)
                        blocks.append(BlobBlock(id=block_id))
                        file_bytes = f.read(block_size)
                    except Exception as e:
                        try:
                            attempt += 1
                            error = str(e)
                        finally:
                            e = None
                            del e

                    else:
                        attempt = 1
                        error = None

        if error is None:
            self.blob_service.put_block_list(self.params["ContainerName"], blob_name, blocks)
        else:
            raise Exception("Failed to upload a resource to Azure Blob destination. {0}".format(error))

    @log_method
    def get_uploaded_file_size(self, path_to_file, outid=None):
        res = self.blob_service.get_blob_properties(self.params["ContainerName"], self.destination_path + path_to_file.strip("/"))
        if res:
            return res.properties.content_length
        return 0

    @log_method
    def get_file_names_placed_at_destination(self):
        return [blob.name for blob in self.blob_service.list_blobs(self.params["ContainerName"])]

    @log_method
    def delete_file(self, file_name, outId=None):
        if not self.is_file_exist(file_name):
            raise DestinationFileDoesNotExist
        self.blob_service.delete_blob(self.params["ContainerName"], self.destination_path + file_name)

    def close_connection(self):
        return

    @log_method
    def is_file_exist(self, file_name, outid=None):
        return self.blob_service.exists(self.params["ContainerName"], self.destination_path + file_name)

    @log_method
    def download_file(self, src, dst, outId=None):
        self.blob_service.get_blob_to_path(self.params["ContainerName"], self.destination_path + src, dst + src)

    @log_method
    def test_destination(self, working_dir, file_name):
        self.connect()
        self.send_backup_to_destination(working_dir, file_name)
        try:
            self.delete_file(file_name)
        except DestinationFileDoesNotExist:
            pass

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/azure_destination.pyc
