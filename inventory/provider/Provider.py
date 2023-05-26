#
# Classe Provider
#

class Provider:
    id :str
    name :str
    _resources :dict
    _is_connected :bool

    def __init__(self, id:str, name: str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id
        self._resources = {}
        self._resources['all'] = {}
        self._is_connected = False

    def Connect(self):
        pass

    def IsConnected(self):
        return self._is_connected

    def LoadResources(self) -> dict:
        return self._resources

    def PrintResources(self):
        for k_resource, resource in dict(sorted(self._resources['all'].items())).items():
            resource.print()

    def print(self):
        print("")
        print("=" * (15 + len(self.name)))
        print(f"== Provider {self.name} ==")
        print("=" * (15 + len(self.name)))
        print("")
        print(f"is connected    : {str(self.IsConnected())}")
        print(f"resources count : {len(self._resources['all'])}")
        