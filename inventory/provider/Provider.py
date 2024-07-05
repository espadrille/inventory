#
# Classe Provider
#
from ..Console import console
from ..ConfigurableObject import ConfigurableObject

class Provider(ConfigurableObject):
    _resources :dict
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id:str, name: str="", config :dict={}):
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
        return self.GetProperty('id')

    def ListResources(self):
        datas = []
        for resource in dict(sorted(self._resources['all'].items())).values():
            datas.append([resource.GetProperty('Profile'), resource.GetProperty('Region'), resource.Name(), resource.Description()])
        console.PrintTab(title=f"Provider {self.GetProperty('name')}", headers=["Environnement", "Region", "Name", "Description"], datas=datas)

    def LoadResources(self) -> dict:
        return self._resources
    
    def Name(self):
        return self.GetProperty('name')

    def Print(self):
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Provider {self.GetProperty('name')}", datas=datas, footer="", text_format='YELLOW')

    def PrintResources(self):
        for resource in dict(sorted(self._resources['all'].items())).values():
            resource.Print()
        