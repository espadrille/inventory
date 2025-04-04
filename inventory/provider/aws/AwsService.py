'''
    Module de classe AwsService
'''

#
# Imports
#
from ...core.Console import console
from .AwsClient import AwsClient
from ...core.ConfigurableObject import ConfigurableObject

class AwsService(ConfigurableObject):
    '''
        Classe AwsService
    '''

    _id :str
    _name :str
    _is_regional :bool=True
    _resources :dict
    _clients :list # Liste des clients boto3 associes au service AWS
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, config :dict=None):
        '''
            Constructeur de la classe
        '''
        if config is None:
            config = {}

        super().__init__(config=config)
        self._id = config["id"]
        self._name = config["name"]
        if self._name == "":
            self._name = self._id
        self._resources = {}
        self._resources['all'] = {}

        self._clients = []
        for my_role in self._config["assume_roles"].items():
            if self._is_regional:
                for my_region in self._config["regions"]:
                    self._clients.append(AwsClient(service=self._id, role=my_role, region=my_region))
            else:
                self._clients.append(AwsClient(service=self._id, role=my_role))
        for my_resource_type in self._config["resource_types"]:
            self._resources[my_resource_type] = {}
        self._summary = {}

    #
    # Public methods
    #
    def Id(self):
        '''
            Retourne l'identifiant de l'objet
        '''
        return self._id

    def Name(self):
        '''
            Retourne le nom de l'objet
        '''
        return self._name

    def LoadResources(self) -> dict:
        '''
            Charge les ressources
        '''
        return self._resources

    def Print(self):
        '''
            Affichage de l'objet
        '''
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Client {self._id}", datas=datas, footer="")

    def PrintResources(self):
        '''
            Affichage des ressources
        '''
        for my_resource in self._resources['all'].values():
            my_resource.Print()
