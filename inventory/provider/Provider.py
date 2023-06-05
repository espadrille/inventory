#
# Classe Provider
#
from ..Console import console

class Provider:
    id :str
    name :str
    _resources :dict
    _is_connected :bool
    _summary: dict

    def __init__(self, id:str, name: str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id
        self._resources = {}
        self._resources['all'] = {}
        self._is_connected = False
        self._summary = {}

    def Connect(self):
        pass

    def IsConnected(self):
        return self._is_connected

    def LoadResources(self) -> dict:
        return self._resources

    def PrintResources(self):
        for resource in dict(sorted(self._resources['all'].items())).values():
            resource.print()

    def print(self):
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.print_tab(title=f"Provider {self.name}", datas=datas, footer="")
        