# Interface AWS

#
# Imports
#
from ..provider.Provider import Provider
from .ec2.Ec2 import Ec2
from .rds.Rds import Rds
from .s3.S3 import S3
from ..Console import console

#
# Classe AWS
#
class Aws(Provider):
    _services :list

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict={}):
        super().__init__(id=id, name=name, config=config)

        self._summary['services'] = []
        self._summary['regions'] = []
        self._summary['profiles'] = []

        #
        # Creation des services AWS a analyser
        #
        self._services = []
        if 'services' in self._config:
            for my_service_name, my_service in self._config['services'].items():
                self._summary['services'].append(my_service_name)

                # Creation de la configuration du service
                service_config = my_service

                if 'assume_roles' in self._config:
                    service_config['assume_roles'] = self._config['assume_roles']
                    for my_role_name, my_role_arn in self._config['assume_roles'].items():
                        self._summary['profiles'].append(my_role_name)

                if 'regions' in self._config:
                    service_config["regions"] = self._config['regions']
                    for my_region_name in self._config['regions']:
                        self._summary['regions'].append(my_region_name)

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
