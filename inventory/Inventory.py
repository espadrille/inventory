#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
from importlib import import_module
from .provider.Provider import Provider

#
# Classe d'inventaire
#
class Inventory:
    name = ""
    id = ""
    provider: Provider
    _resources: dict = {}

    def __init__(self, id:str="", name: str="", provider: str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id
        self.SetProvider(provider=provider)

    def LoadResources(self):
        self._resources = self.provider.LoadResources()
        return self._resources
    
    def SetProvider(self, provider: str="") -> Provider:
        if provider == "Aws":
            from .aws.Aws import Aws
            self.provider = Aws(id="aws", name="AWS", service_names=['ec2'])
        else:
            self.provider = Provider(id="unknown")
        return self.provider
    
    def PrintResources(self):
        for k_resource, resource in self._resources['all'].items():
            resource.print()

    def print(self):
        print("")
        print("=" * (16 + len(self.name)))
        print(f"== Inventaire {self.name} ==")
        print("=" * (16 + len(self.name)))
        print("")
        print(f"id              : {self.id}")
        print(f"resources count : {len(self._resources['all'])}")
        self.provider.print()
        