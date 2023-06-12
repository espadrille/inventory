# Interface AWS

#
# Imports
#
import boto3
from ..provider.Provider import Provider
from .Ec2 import Ec2
from .Rds import Rds
from .S3 import S3
from .AwsService import AwsService
from ..Console import console

#
# Classe AWS
#
class Aws(Provider):
    _config: dict
    _profile_names :list
    _region_names :list
    _service_names :list
    _clients :dict = {}

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict={}):
        super().__init__(id=id, name=name)
        self._config = config
        self._config['global_services'] = ['s3']
        self._config['regional_services'] = ['ec2', 'rds']

        # Liste des services AWS a analyser
        self._service_names = boto3.Session().get_available_services()
        if "filters" in self._config:
            if "services" in self._config["filters"]:
                if len(self._config["filters"]["services"]) > 0:
                    self._service_names = self._config["filters"]["services"]
        self._summary['services'] = self._service_names

        # Liste des regions AWS a analyser
        self._region_names = []
        for my_service_name in self._service_names:
            for my_region_name in boto3.Session().get_available_regions(my_service_name):
                if not my_region_name in self._region_names:
                    self._region_names.append(my_region_name)
        if "filters" in self._config:
            if "regions" in self._config["filters"]:
                if len(self._config["filters"]["regions"]) > 0:
                    self._region_names = self._config["filters"]["regions"]
        self._summary['regions'] = self._region_names

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
        self._summary['profiles'] = self._profile_names

    #
    # Public methods
    #
    def Connect(self):
        for my_profile in self._profile_names:
            try:
                test_session = boto3.Session(profile_name=my_profile)
                self._is_connected = True
            except:
                print(f"Impossible de se connecter sur le profile {my_profile}")
        self._summary['is connected'] = self._is_connected

    def LoadResources(self) -> dict:
        if not self.IsConnected():
            self.Connect()


        for my_profile in self._profile_names:
            self._resources[my_profile] = {}
            self._resources[my_profile]['all'] = {}

            new_session = boto3.Session(profile_name=my_profile) # Une session par profile

            for my_service in self._service_names:

                self._resources[my_service] = {}
                self._resources[my_service]['all'] = {}

                if my_service in self._config['regional_services']:  # Liste des services regionaux
                    for my_region in self._region_names:
                        self._resources[my_region] = {}
                        self._resources[my_region]['all'] = {}

                        new_client = new_session.client(service_name=my_service, region_name=my_region) # Un client par service et par region

                        if my_service == 'ec2':
                            self._clients[f"{my_profile}.{my_service}.{my_region}"] = Ec2(session=new_session, client=new_client) # type: ignore
                        elif my_service == 'rds':
                            self._clients[f"{my_profile}.{my_service}.{my_region}"] = Rds(session=new_session, client=new_client) # type: ignore

                elif my_service in self._config['global_services']:  # Liste des services non regionaux
                    self._resources['any'] = {}
                    self._resources['any']['all'] = {}

                    new_client = new_session.client(service_name=my_service) # Un client par service

                    if my_service == 's3':
                        self._clients[f"{my_profile}.{my_service}"] = S3(session=new_session, client=new_client) # type: ignore

        # Chargement des resources
        for my_client in self._clients.values():
            console.Print(f"   ==> Chargement : {my_client.Profile()} - {my_client.Name()} - {my_client.Region()} : ", newline=False)
            client_resources = my_client.LoadResources()
            console.Print(f" {len(client_resources['all'])} resources. <==")
            
            for my_resource_key, my_resource in client_resources['all'].items():
                self._resources[my_client.Profile()]['all'][my_resource_key] = my_resource
                self._resources[my_client.Name()]['all'][my_resource_key] = my_resource
                self._resources[my_client.Region()]['all'][my_resource_key] = my_resource
                self._resources['all'][my_resource_key] = my_resource

        self._summary['resources total'] = str(len(self._resources['all']))

        return self._resources

    def Print(self):
        for key, value in self._resources.items():
            if 'all' in value:
                self._summary[f"resources {key}"] = str(len(value['all']))
        super().Print()
        for my_client in self._clients.values():
            my_client.Print()
