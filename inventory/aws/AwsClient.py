#
# Classe AwsResource
#
import boto3
from ..Console import console
from ..Object import Object

class AwsClient(Object):
    _boto3_client: boto3.client.__class__
    _boto3_session: boto3.Session

    #
    # Private methods
    #
    def __init__(self, service: str, profile: str, region:str=""):
        super().__init__()
        self._properties['service'] = service
        self._properties['profile'] = profile
        self._properties['region'] = region

        self._boto3_session = boto3.Session(profile_name=self._properties['profile']) # Une session par profile

        if region == "":
            self._boto3_client = self._boto3_session.client(service_name=self._properties['service']) # type: ignore
        else:
            self._boto3_client = self._boto3_session.client(service_name=self._properties['service'], region_name=self._properties['region']) # type: ignore

        console.Debug(f"Creation client : {self.Name()}")

    #
    # Public methods
    #
    def Client(self):
        return self._boto3_client
    
    def Name(self):
        if self._properties['region'] == "":
            return f"{self._properties['service']}.{self._properties['profile']}"
        else:
            return f"{self._properties['service']}.{self._properties['profile']}.{self._properties['region']}"
    
    def Profile(self):
        return self._properties['profile']

    def Region(self):
        return self._properties['region']

    def Service(self):
        return self._properties['service']
