# Interface AWS

#
# Imports
#
import boto3
from ..provider.Provider import Provider
from .Ec2 import Ec2
from .Rds import Rds
from .S3 import S3

#
# Classe AWS
#
class Aws(Provider):
    _profiles :list
    _service_names :list
    _services :dict

    def __init__(self, id:str, name: str="", service_names :list=[]):
        super().__init__(id=id, name=name)
        self._profiles = []
        if service_names == []:
            self._service_names = ['ec2', 'rds', 's3']
        else:
            self._service_names = service_names
        self._services = {}

    def Connect(self):
        try:
            for my_profile in boto3.Session().available_profiles:
                self._profiles.append(my_profile) 
            self._profiles = ['developpement']
        except:
            print(f"Impossible de lire les profiles AWS")

        for profile in self._profiles:
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

            for profile in self._profiles:
                service_resources = self._services[my_service_name].LoadResources(profile_name=profile)
                    
                for my_resource_key, my_resource in service_resources['all'].items():
                    self._resources['all'][my_resource_key] = my_resource
                    self._resources[my_service_name]['all'][my_resource_key] = my_resource

        return self._resources

    def print(self):
        super().print()
        print(f"profiles        : {self._profiles}")
        services_names = []
        for my_service in self._services.values():
            services_names.append(my_service.name)
        print(f"services        : {services_names}")
        for my_service in self._services.values():
            my_service.print()
            my_service.PrintResources()
