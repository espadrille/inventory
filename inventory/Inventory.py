#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
from importlib import import_module

#
# Classe d'inventaire
#
class Inventory:
    provider = None

    def __init__(self, provider=""):
        self.SetProvider(provider=provider)

    def Connect(self):
        self.provider.Connect()
    
    def LoadResources(self):
        self.provider.LoadResources()
    
    def SetProvider(self, provider=""):
        if provider == "Aws":
            from aws.Aws import Aws
            self.provider = Aws()

    def print(self):
        self.provider.print()
        