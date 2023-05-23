# Service AWS

#
# Imports
#
import boto3

#
# Classe Service
#
class Service:
    id :str
    name :str
    _profile :str
    regions :list
    _resources :dict
    _client :boto3.client.__class__
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, id: str, name: str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id.upper()
        self.regions = boto3.Session().get_available_regions(self.id)
        self.profile = ""
        self._resources = {}
        self._resources['all'] = {}
        for my_resource_type in self._resource_types:
            self._resources[my_resource_type] = {}
    
    def SetProfile(self, profile_name: str):
        self._profile = profile_name

    def LoadResources(self, profile_name: str) -> dict:
        self.SetProfile(profile_name=profile_name)
        return self._resources

    def PrintResources(self):
        for k_resource, resource in self._resources['all'].items():
            resource.print()

    def print(self):
        print("")
        print("=================")
        print(f"== Service {self.name.upper()} ==")
        print("=================")
        print("")
        print(f"id              : {self.id}")
        for my_resource_category in self._resources:
            print(f"{my_resource_category} count : {len(self._resources[my_resource_category])}")
