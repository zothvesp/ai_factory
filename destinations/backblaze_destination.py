import base64, json, certifi, urllib.request, ssl
from sqlbak.destinations.amazon_compatible import AmazonCompatibleDestination
from sqlbak.logger import log_error, log_method, log_data

class BackblazeDestination(AmazonCompatibleDestination):

    def __init__(self, params):
        self.access_key = params["AccessKey"].strip("")
        self.secret_key = params["SecretKey"].strip("")
        self.params = params
        self.params["AuthenticationRegion"] = ""
        super().__init__(params)

    @log_method
    def GetS3EndPointParse error at or near `SETUP_FINALLY' instruction at offset 0

    def connect(self):
        self.params["EndPoint"] = self.GetS3EndPoint
        super().connect
