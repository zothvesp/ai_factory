import json
import xml.etree.ElementTree as Et
from sqlbak.definitions import DESTINATIONS_CONSTS, FTP_PROTOCOLS, MINUTE_IN_SEC
from sqlbak.destinations.amazon_destination import AmazonDestination
from sqlbak.destinations.azure_destination import AzureDestination
from sqlbak.destinations.drop_box_destination import DropBoxDestination
from sqlbak.destinations.folder_destination import FolderDestination
from sqlbak.destinations.ftp_destination import FTPDestination
from sqlbak.destinations.google_destination import GoogleDestination
from sqlbak.destinations.one_drive_destination import OneDriveDestination
from sqlbak.destinations.amazon_compatible import AmazonCompatibleDestination
from sqlbak.destinations.backblaze_destination import BackblazeDestination
from sqlbak.helper import Helper
from sqlbak.logger import log_method
from sqlbak.local_db import LocalDB
import base64, binascii

class Destination:

    def __init__(self):
        self.local_db = LocalDB()
        self.helper = Helper()

    @log_method
    def get_job_destination_instances(self, job_id):
        return [self.get_destination_instance(jd) for jd in self.local_db.get_job_destinations(job_id)]

    @log_method
    def get_destination_instance(self, job_destination):
        destination_settings = self.get_destination_settings(job_destination)
        destination_class = self.get_destination_class(job_destination["DestinationType"])
        return destination_class(destination_settings)

    @log_method
    def get_destination_class(self, destination_type):
        """
        Method to get a destination class according to a destination
        :param destination_type: str;
        :return: destination class or none
        """
        func = {(DESTINATIONS_CONSTS["FOLDER"]): FolderDestination, 
         (DESTINATIONS_CONSTS["DROPBOX"]): DropBoxDestination, 
         (DESTINATIONS_CONSTS["FTP"]): FTPDestination, 
         (DESTINATIONS_CONSTS["AMAZON"]): AmazonDestination, 
         (DESTINATIONS_CONSTS["AZURE"]): AzureDestination, 
         (DESTINATIONS_CONSTS["ONEDRIVE"]): OneDriveDestination, 
         (DESTINATIONS_CONSTS["GOOGLE"]): GoogleDestination, 
         (DESTINATIONS_CONSTS["BACKBLAZE"]): GoogleDestination, 
         (DESTINATIONS_CONSTS["ONEDRIVE_BUSINESS"]): OneDriveDestination, 
         (DESTINATIONS_CONSTS["AMAZON_S3_COMP"]): AmazonCompatibleDestination, 
         (DESTINATIONS_CONSTS["BACKBLAZE"]): BackblazeDestination}
        if destination_type in func:
            return func[destination_type]
        raise Exception("There is no an appropriate destination for {0} a destination type".format(destination_type))

    @log_method
    def get_destination_handler_by_destination_type(self, destination_type):
        func = {(DESTINATIONS_CONSTS["FOLDER"]): (self.get_folder_destination_settings), 
         (DESTINATIONS_CONSTS["FTP"]): (self.get_ftp_destination_settings), 
         (DESTINATIONS_CONSTS["AMAZON"]): (self.get_amazon_destination_settings), 
         (DESTINATIONS_CONSTS["AZURE"]): (self.get_azure_destination_settings), 
         (DESTINATIONS_CONSTS["DROPBOX"]): (self.get_dropbox_destination_settings), 
         (DESTINATIONS_CONSTS["ONEDRIVE"]): (self.get_one_drive_destination_settings), 
         (DESTINATIONS_CONSTS["GOOGLE"]): (self.get_google_destination_settings), 
         (DESTINATIONS_CONSTS["BACKBLAZE"]): (self.get_backblaze_destination_settings), 
         (DESTINATIONS_CONSTS["YANDEX"]): (self.get_yandex_destination_settings), 
         (DESTINATIONS_CONSTS["BOX"]): (self.get_box_destination_settings), 
         (DESTINATIONS_CONSTS["ONEDRIVE_BUSINESS"]): (self.get_one_drive_destination_settings), 
         (DESTINATIONS_CONSTS["AMAZON_S3_COMP"]): (self.get_amazon_compatible_destination_settings)}
        if destination_type in func:
            return func[destination_type]
        raise Exception("There is no an appropriate destination for {0} a destination type".format(destination_type))

    @log_method
    def test_destination(self, data, working_dir, file_name):
        data["DestinationInfo"].update({"DestinationPath": (data["Parameters"]["Path"] if "Parameters" in data else "")})
        destination_instance = self.get_destination_instance(data["DestinationInfo"])
        self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "test_destination", is_instance=True, params=(working_dir, file_name), attempts=4, time_out=(5 * MINUTE_IN_SEC))

    @log_method
    def test_sftp_destination(self, data):
        data["DestinationInfo"].update({"DestinationPath": (data["Parameters"]["Path"] if "Parameters" in data else "")})
        destination_instance = self.get_destination_instance(data["DestinationInfo"])
        finger_print = self.helper.run_method_with_number_attempts_and_timeout(destination_instance, "test_sftp_destination", is_instance=True, attempts=4, time_out=(5 * MINUTE_IN_SEC))
        return finger_print

    @log_method
    def get_destination_settings(self, destination_info):
        """
        Method to get a destination class according to a destination
        :param destination_info: str;
        :return: destination class or none
        """
        if "DestinationConfiguration" in destination_info:
            destination_info = self.get_destination_config_settings(destination_info)
        handler = self.get_destination_handler_by_destination_type(destination_info["DestinationType"])
        destination_info.update(handler(destination_info))
        return destination_info

    @log_method
    def handle_access_info(self, access_info):
        if "nonce" in access_info:
            access_info = self.helper.decrypt_string(access_info)
        return Et.fromstring(access_info.encode("utf-16"))

    @log_method
    def get_destination_config_settings(self, settings):
        config = Et.fromstring(settings["DestinationConfiguration"].encode("utf-16"))
        settings = self.get_destination_path(config, settings)
        settings = self.check_if_destination_extreme(config, settings)
        for root in config:
            if root.tag == "KeepInfo":
                settings = self.keep_info(root, settings)
            elif root.tag == "IncKeepInfo":
                settings = self.get_inc_keep_info(root, settings)
            elif root.tag == "VerificationAfterUploading":
                settings = self.check_if_should_verify(root, settings)
            else:
                if root.tag == "BackupTypes":
                    settings = self.get_backup_types(root, settings)
                return settings

    @log_method
    def get_destination_path(self, config, settings):
        settings["DestinationPath"] = config.attrib["Path"] if "Path" in config.attrib else ""
        return settings

    @log_method
    def check_if_destination_extreme(self, config, settings):
        if "JobDestinationType" in config.attrib:
            settings["IsExtreme"] = 1 if config.attrib["JobDestinationType"] == "Emergency" else 0
        else:
            settings["IsExtreme"] = 0
        return settings

    @log_method
    def keep_info(self, root, settings):
        settings.update({'KeepMonths':int(root.attrib["KeepMonths"]) if ("KeepMonths" in root.attrib) else 0, 
         'KeepDays':int(root.attrib["KeepDays"]) if ("KeepDays" in root.attrib) else 0})
        return settings

    @log_method
    def get_inc_keep_info(self, root, settings):
        settings.update({'IncKeepMonths':int(root.attrib["KeepMonths"]) if ("KeepMonths" in root.attrib) else 0, 
         'IncKeepDays':int(root.attrib["KeepDays"]) if ("KeepDays" in root.attrib) else 0})
        return settings

    @log_method
    def check_if_should_verify(self, root, settings):
        settings["VerifyFile"] = self.helper.is_text_true(root.attrib["VerifyFile"]) if "VerifyFile" in root.attrib else False
        return settings

    @log_method
    def get_backup_types(self, root, settings):
        settings["SendBackupTypes"] = []
        for child in root:
            if child.tag == "BackupType" and "BackupType" in child.attrib:
                settings["SendBackupTypes"].append(int(child.attrib["BackupType"]))
            return settings

    @log_method
    def get_folder_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        return {"DestinationPath": (d.attrib["Path"])}

    @log_method
    def get_ftp_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        access = self.handle_access_info(settings["AccessInfo"])
        params = {'VerifyServerFingerprint':False, 
         'ServerFingerprint':""}
        for child in d:
            if child.tag == "FtpSettings":
                if "ServerFingerprint" in child.attrib:
                    finger_print = binascii.hexlify(bytearray(base64.b64decode(child.attrib["ServerFingerprint"]))).decode("utf-8")
                else:
                    finger_print = ""
                params.update({'VerifyServerFingerprint':self.helper.is_text_true(child.attrib["VerifyServerFingerprint"]) if ("VerifyServerFingerprint" in child.attrib) else False, 
                 'ServerFingerprint':finger_print})
            params.update({'DestinationPassword':access.attrib["Password"] if ("Password" in access.attrib) else "", 
             'DestinationUser':access.attrib["UserName"], 
             'DestinationHost':d.attrib["HostName"], 
             'DestinationFtpProtocol':d.attrib["Protocol"].lower() if ("Protocol" in d.attrib) else (FTP_PROTOCOLS["FTP"]), 
             'DestinationPort':d.attrib["Port"] if ("Port" in d.attrib) else 21, 
             'SslMode':d.attrib["SslMode"] if ("SslMode" in d.attrib) else None, 
             'SFtpAuthenticationMethod':access.attrib["SFtpAuthenticationMethod"] if ("SFtpAuthenticationMethod" in access.attrib) else "Password", 
             'SshPrivateKey':base64.b64decode(access.attrib["SshPrivateKey"]).decode("utf-8") if ("SshPrivateKey" in access.attrib) else ""})
            return params

    @log_method
    def get_amazon_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        access = self.handle_access_info(settings["AccessInfo"])
        return {'SecretKey':access.attrib["SecretKey"], 
         'AccessKey':access.attrib["AccessKey"], 
         'UseSsl':(self.helper.is_text_true)(d.attrib["UseSsl"]), 
         'BucketName':d.attrib["BucketName"]}

    @log_method
    def get_azure_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        access = self.handle_access_info(settings["AccessInfo"])
        return {'ContainerName':d.attrib["ContainerName"], 
         'AccountName':access.attrib["AccountName"], 
         'AccountKey':access.attrib["AccountKey"]}

    @log_method
    def get_dropbox_destination_settings(self, settings):
        token = self.get_access_token_by_xml_settings(settings)
        if token:
            return {"AccessToken": token}
        return {}

    @log_method
    def get_one_drive_destination_settings(self, settings):
        token = self.get_access_token_by_xml_settings(settings)
        if token:
            return {"AccessToken": token}
        return {}

    @log_method
    def get_google_destination_settings(self, settings):
        token = self.get_access_token_by_xml_settings(settings)
        if token:
            return {"AccessToken": token}
        return {}

    def get_backblaze_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        access = self.handle_access_info(settings["AccessInfo"])
        account_id = access.attrib["AccountId"]
        application_key = access.attrib["ApplicationKey"]
        bucket_name = d.attrib["BucketName"]
        return {
         'AccessKey': account_id, 
         'SecretKey': application_key, 
         'BucketName': bucket_name, 
         'ConcurrentUpload': False}

    def get_box_destination_settings(self, settings):
        return

    def get_yandex_destination_settings(self, settings):
        return

    def get_amazon_compatible_destination_settings(self, settings):
        d = Et.fromstring(settings["DestinationSettings"].encode("utf-16"))
        access = self.handle_access_info(settings["AccessInfo"])
        return {'SecretKey':access.attrib["SecretKey"], 
         'AccessKey':access.attrib["AccessKey"], 
         'ConcurrentUpload':(self.helper.is_text_true)(d.attrib["SupportConcurrentUpload"]), 
         'BucketName':d.attrib["BucketName"], 
         'EndPoint':d.attrib["EndPoint"], 
         'PresetType':d.attrib["PresetType"], 
         'AuthenticationRegion':d.attrib["AuthenticationRegion"] if ("AuthenticationRegion" in d.attrib) else ""}

    @log_method
    def get_access_token_by_xml_settings(self, settings):
        token = None
        access = self.handle_access_info(settings["AccessInfo"])
        for root in access:
            if root.tag == "TokenInfo" and "AccessToken" in root.attrib:
                token = root.attrib["AccessToken"]
            return token

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/destinations/destination.pyc
