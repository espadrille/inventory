# Service AWS

#
# Imports
#
import boto3
from ..Console import console

#
# Classe AwsService
#
class AwsService:
    _id :str
    _name :str
    _profile :str
    _region :str
    _is_regional :bool=True
    _resources :dict
    _client :boto3.client.__class__
    _resource_types : list # Liste des types de ressources a lister pour le service
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id: str, name: str, session, client: boto3.client.__class__):
        self.id = id
        self._name = name
        if name == "":
            self._name = self.id
        self._profile = session.profile_name
        self._region = client._client_config.region_name
        self._resources = {}
        self._resources['all'] = {}
        self._client = client
        for my_resource_type in self._resource_types:
            self._resources[my_resource_type] = {}
        self._summary = {}
        self._is_regional = True
    
    #
    # Public methods
    #
    def Id(self):
        return self._id
    
    def Name(self):
        return self._name

    def LoadResources(self) -> dict:
        return self._resources

    def Print(self):
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Client {self.id}", datas=datas, footer="")

    def PrintResources(self):
        for my_resource in self._resources['all'].values():
            my_resource.print()

    def Profile(self):
        return self._profile

    def Region(self):
        if self._is_regional:
            return self._region
        else:
            return "any"
