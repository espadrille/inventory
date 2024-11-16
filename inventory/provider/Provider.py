'''
    Provider
'''

from ..Console import console
from ..ConfigurableObject import ConfigurableObject

class Provider(ConfigurableObject):
    '''
        Classe Provider
    '''

    _resources :dict
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict=None):
        if config is None:
            config = {}
        super().__init__(config=config)
        self.SetProperty('id', id)
        self.SetProperty('name', name)
        if name == "":
            self.SetProperty('name', self.GetProperty('id'))
        self._resources = {}
        self._resources['all'] = {}
        self._summary = {}

    #
    # Public methods
    #
    def Id(self):
        '''
            Identifiant du provider
        '''
        return self.GetProperty('id')

    def ListResources(self):
        '''
            Liste des ressources associees au provider
        '''
        
        datas = []
        for resource in dict(sorted(self._resources['all'].items())).values():
            datas.append([resource.GetProperty('Profile'), resource.GetProperty('Region'), resource.Name(), resource.Description()])
        console.PrintTab(title=f"Provider {self.GetProperty('name')}", headers=["Environnement", "Region", "Name", "Description"], datas=datas)

    def LoadResources(self) -> dict:
        '''
            Chargement des ressources associees au rpovider
        '''
        
        return self._resources

    def Name(self):
        '''
            Nom du porvider
        '''
        
        return self.GetProperty('name')

    def Print(self):
        '''
            Affichage des informations du provider
        '''
        
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Provider {self.GetProperty('name')}", datas=datas, footer="", text_format='YELLOW')

    def PrintResources(self):
        '''
            Affichage de la liste des ressources associees au provider
        '''
        
        for resource in dict(sorted(self._resources['all'].items())).values():
            resource.Print()
