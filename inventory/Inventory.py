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

    def __init__(self, provider="Aws"):
        if provider == "Aws":
            from aws.Aws import Aws
            self.provider = Aws()

    def print(self):
        # print(self.provider)
        self.provider.print()
        