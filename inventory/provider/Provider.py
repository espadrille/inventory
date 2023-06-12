#
# Classe Provider
#
from ..Console import console

class Provider:
    _id :str
    _name :str
    _resources :dict
    _is_connected :bool
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id:str, name: str=""):
        self._id = id
        self._name = name
        if name == "":
            self.name = self._id
        self._resources = {}
        self._resources['all'] = {}
        self._is_connected = False
        self._summary = {}

    #
    # Public methods
    #
    def Connect(self):
        pass
    
    def Id(self):
        return self._id

    def IsConnected(self):
        return self._is_connected

    def LoadResources(self) -> dict:
        return self._resources
    
    def Name(self):
        return self._name

    def Print(self):
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Provider {self._name}", datas=datas, footer="")

    def PrintResources(self):
        for resource in dict(sorted(self._resources['all'].items())).values():
            resource.Print()
        