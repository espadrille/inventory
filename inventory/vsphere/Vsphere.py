# Interface AWS

#
# Imports
#
from ..provider.Provider import Provider
from ..Console import console
from .datacenter.Datacenter import Datacenter

#
# Classe AWS
#
class Vsphere(Provider):
    _datacenters :list

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict={}):
        super().__init__(id=id, name=name)
        self._config = config

        self._summary['datacenters'] = []

        #
        # Creation des services VSphere a analyser
        #
        self._datacenters = []
        if 'datacenter_credentials' in self._config:
            for my_datacenter_name, my_datacenter_config in self._config['datacenter_credentials'].items():
                self._summary['datacenters'].append(my_datacenter_name)

                # Creation des objets Datacenter dans self._datacenters
                self._datacenters.append(Datacenter(name=my_datacenter_name, config=my_datacenter_config | {'folders': config['folders']}))



    #
    # Public methods
    #
    def LoadResources(self) -> dict:
        console.Debug(f"Chargement : VSphere")
        self._resources['all'] = {}
        for my_datacenter in self._datacenters:
            console.Debug(f" Chargement : {my_datacenter.Name()}")
            self._resources[my_datacenter.Name()] = my_datacenter.LoadResources()
            for my_resource_key, my_resource in self._resources[my_datacenter.Name()]['all'].items():
                self._resources['all'][my_resource_key] = my_resource
            console.Debug(f"  ==> Total : {my_datacenter.Name()} : {len(self._resources[my_datacenter.Name()]['all'])} resources.")

        self._summary['resources total'] = str(len(self._resources['all']))
        console.Debug(f" ==> Total VSphere : {len(self._resources['all'])} resources.")

        return self._resources

    def Print(self):
        for key, value in self._resources.items():
            if 'all' in value:
                self._summary[f"resources {key}"] = str(len(value['all']))
        super().Print()
