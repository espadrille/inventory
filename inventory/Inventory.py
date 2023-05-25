#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
import json
import mimetypes
import os
from importlib import import_module
from .provider.Provider import Provider

#
# Classe d'inventaire
#
class Inventory:
    name = ""
    id = ""
    _config: dict
    _config_file: str
    _providers: dict
    _resources: dict

    def __init__(self, id:str="", name: str="", providers: list=[], config_file :str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id

        self._providers = {}
        self._resources = {}
        self._resources['all'] = {}
        self._config = {}
        self._config_file = ""

        # Chargement de la configuration
        if os.path.isfile(f"{config_file}"):
            self._config_file = f"{config_file}"
        if os.path.isfile(f"{os.getcwd()}/{config_file}"):
            self._config_file = f"{os.getcwd()}/{config_file}"
        if os.path.isfile(f"{os.path.dirname(__file__)}/{config_file}"):
            self._config_file = f"{os.path.dirname(__file__)}/{config_file}"

        if self._config_file == "":
            print(f"Fichier de configuration non trouve [{config_file}]")
        else:
            self.LoadConfig()
  
        # Creation des providers
        for my_provider in providers:
            self._resources[my_provider] = {}
            self.AddProvider(provider=my_provider)

    def LoadConfig(self):
        try:
            config_file_mime_type = mimetypes.guess_type(self._config_file)[0]
            fp = open(self._config_file, "r")
            if config_file_mime_type == "application/json":
                try:
                    self._config = json.loads(fp.read())
                except Exception as e:
                    print(f"Format json incorrect dans le fichier [{self._config_file}", "ERROR")
                    print(e.__str__())
            else:
                print(f"Format non pris en charge : {str(config_file_mime_type)}")
            fp.close()
        except Exception as e:
            print(f"Impossible de charger le fichier de configuration [{self._config_file}]")
            print(e.__str__())

    def LoadResources(self) -> dict:
        for my_provider_key, my_provider in self._providers.items():
            self._resources[my_provider_key] = my_provider.LoadResources()
            for resource_key, resource in self._resources[my_provider_key]['all'].items():
                self._resources['all'][resource_key] = resource
        return self._resources
    
    def AddProvider(self, provider: str=""):
        if provider == "AWS":
            provider_config = {}
            if self._config_file != "":
                if "inventory" in self._config:
                    if "providers" in self._config["inventory"]:
                        if "aws" in self._config["inventory"]["providers"]:
                            provider_config = self._config["inventory"]["providers"]["aws"]
            from .aws.Aws import Aws
            self._providers[provider] = Aws(id="aws", name="AWS", config=provider_config)
        else:
            self._providers['other'] = Provider(id="unknown")
    
    def PrintResources(self):
        for resource in self._resources['all'].values():
            resource.print()

    def print(self):
        print("")
        print("=" * (16 + len(self.name)))
        print(f"== Inventaire {self.name} ==")
        print("=" * (16 + len(self.name)))
        print("")
        print(f"id              : {self.id}")
        print(f"resources count : {len(self._resources['all'])}")
        for my_provider in self._providers.values():
            my_provider.print()
        