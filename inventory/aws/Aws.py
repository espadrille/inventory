# Interface AWS

#
# Imports
#
import boto3
from ..provider.Provider import Provider
from .ec2.Ec2 import Ec2
from .rds.Rds import Rds
from .s3.S3 import S3
from ..Console import console

#
# Classe AWS
#
class Aws(Provider):
    _config: dict
    _filtered_profile_names :list
    _filtered_region_names :list
    _filtered_services_names :list
    _services :list

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict={}):
        super().__init__(id=id, name=name)
        self._config = config

        # Filtrage des services AWS a analyser
        self._filtered_services_names = boto3.Session().get_available_services()
        if "filters" in self._config:
            if "services" in self._config["filters"]:
                if len(self._config["filters"]["services"]) > 0:
                    self._filtered_services_names = self._config["filters"]["services"]
        self._summary['services'] = self._filtered_services_names

        # Filtrage des regions AWS a analyser
        self._filtered_region_names = []
        for my_service_name in self._filtered_services_names:
            for my_region_name in boto3.Session().get_available_regions(my_service_name):
                if not my_region_name in self._filtered_region_names:
                    self._filtered_region_names.append(my_region_name)
        if "filters" in self._config:
            if "regions" in self._config["filters"]:
                if len(self._config["filters"]["regions"]) > 0:
                    self._filtered_region_names = self._config["filters"]["regions"]
        self._summary['regions'] = self._filtered_region_names

        # Filtrage des profiles a analyser
        self._filtered_profile_names = []
        try:
            for my_profile in boto3.Session().available_profiles:
                self._filtered_profile_names.append(my_profile) 
        except:
            self._filtered_profile_names = []
        if "filters" in self._config:
            if "profiles" in self._config["filters"]:
                if len(self._config["filters"]["profiles"]) > 0:
                    self._filtered_profile_names = self._config["filters"]["profiles"]
        self._summary['profiles'] = self._filtered_profile_names

        #
        # Creation des services AWS a analyser
        #
        self._services = []
        for my_service_name in self._filtered_services_names:

            # Creation de la configuration du service
            service_config = {}
            if "services" in self._config:
                if my_service_name in self._config["services"]:
                    service_config = self._config["services"][my_service_name]
            service_config["profiles"] = self._filtered_profile_names
            service_config["regions"] = self._filtered_region_names

            # Creation des objets AwsService dans self._services
            if my_service_name == 'ec2':
                self._services.append(Ec2(config=service_config))
            elif my_service_name == 'rds':
                self._services.append(Rds(config=service_config))
            elif my_service_name == 's3':
                self._services.append(S3(config=service_config))


    #
    # Public methods
    #
    def LoadResources(self) -> dict:
        console.Debug(f"Chargement : AWS")
        self._resources['all'] = {}
        for my_service in self._services:
            console.Debug(f" Chargement : {my_service.Name()}")
            self._resources[my_service.Name()] = my_service.LoadResources()
            for my_resource_key, my_resource in self._resources[my_service.Name()]['all'].items():
                self._resources['all'][my_resource_key] = my_resource
            console.Debug(f"  ==> Total : {my_service.Name()} : {len(self._resources[my_service.Name()]['all'])} resources.")

        self._summary['resources total'] = str(len(self._resources['all']))
        console.Debug(f" ==> Total AWS : {len(self._resources['all'])} resources.")

        return self._resources

    def Print(self):
        for key, value in self._resources.items():
            if 'all' in value:
                self._summary[f"resources {key}"] = str(len(value['all']))
        super().Print()
