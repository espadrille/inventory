# Interface AWS

#
# Imports
#
import boto3
from ..provider.Provider import Provider
from .Ec2 import Ec2
from .Rds import Rds
from .S3 import S3
from .Service import Service

#
# Classe AWS
#
class Aws(Provider):
    _profile_names :list
    _service_names :list
    _services :dict
    _config: dict

    def __init__(self, id:str, name: str="", config :dict={}):
        super().__init__(id=id, name=name)
        self._config = config

        # Liste des services AWS a analyser
        self._service_names = ['ec2', 'rds', 's3']
        if "filters" in self._config:
            if "services" in self._config["filters"]:
                if len(self._config["filters"]["services"]) > 0:
                    self._service_names = self._config["filters"]["services"]
        self._services = {}

        # Liste des profiles a analyser
        self._profile_names = []
        try:
            for my_profile in boto3.Session().available_profiles:
                self._profile_names.append(my_profile) 
        except:
            self._profile_names = []
        if "filters" in self._config:
            if "profiles" in self._config["filters"]:
                if len(self._config["filters"]["profiles"]) > 0:
                    self._profile_names = self._config["filters"]["profiles"]

    def Connect(self):
        for profile in self._profile_names:
            try:
                test_session = boto3.Session(profile_name=profile)
                self._is_connected = True
            except:
                print(f"Impossible de se connecter sur le profile {profile}")

    def LoadResources(self) -> dict:
        if not self.IsConnected():
            self.Connect()

        for my_service_name in self._service_names:
            self._resources[my_service_name] = {}
            self._resources[my_service_name]['all'] = {}

            if not my_service_name in self._services:
                if my_service_name == 'ec2':
                        self._services[my_service_name] = Ec2(id=f"{self.id}_ec2", name=my_service_name.upper())
                elif my_service_name == 'rds':
                    self._services[my_service_name] = Rds(id=f"{self.id}_rds", name=my_service_name.upper())
                elif my_service_name == 's3':
                    self._services[my_service_name] = S3(id=f"{self.id}_s3", name=my_service_name.upper())
                else:
                    self._services[my_service_name] = Service(id=f"{self.id}_other", name=my_service_name.upper())

            for profile in self._profile_names:
                service_resources = self._services[my_service_name].LoadResources(profile_name=profile)
                    
                for my_resource_key, my_resource in service_resources['all'].items():
                    self._resources['all'][my_resource_key] = my_resource
                    self._resources[my_service_name]['all'][my_resource_key] = my_resource

        return self._resources

    def print(self):
        super().print()
        print(f"profiles        : {self._profile_names}")
        print(f"services        : {self._service_names}")
        for my_service in self._services.values():
            my_service.print()
