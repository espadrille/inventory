#
# Classe AwsResource
#
import boto3
from ..Console import console

class AwsClient():
    _boto3_client: boto3.client.__class__
    _boto3_session: boto3.Session
    _profile: str
    _region: str
    _service: str

    #
    # Private methods
    #
    def __init__(self, service: str, profile: str, region:str=""):
        self._service = service
        self._profile = profile
        self._region = region

        self._boto3_session = boto3.Session(profile_name=self._profile) # Une session par profile

        if region == "":
            self._boto3_client = self._boto3_session.client(service_name=self._service) # type: ignore
        else:
            self._boto3_client = self._boto3_session.client(service_name=self._service, region_name=self._region) # type: ignore

        console.Debug(f"Creation client : {self.Name()}")

    #
    # Public methods
    #
    def Client(self):
        return self._boto3_client
    
    def Name(self):
        if self._region == "":
            return f"{self._service}.{self._profile}"
        else:
            return f"{self._service}.{self._profile}.{self._region}"
    
    def Profile(self):
        return self._profile

    def Region(self):
        return self._region

    def Service(self):
        return self._service
