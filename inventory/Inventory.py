#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
import json
import mimetypes
import os
from .Console import console
from .provider.Provider import Provider
from .CustomJSONEncoder import CustomJSONEncoder

#
# Classe d'inventaire
#
class Inventory:
    _name: str = ""
    _id: str = ""
    _config: dict
    _config_file: str
    _output_mode: str
    _output_file: str
    _output_format: str
    _providers: dict
    _resources: dict

    #
    # Private methods
    #
    def __init__(self, id:str="", name: str="", providers: list=[], config_file :str=""):

        self._id = id
        self._name = name
        if name == "":
            self._name = self._id

        self._output_mode = "console"
        self._output_format = "table"
        self._output_file = ""
        self._providers = {}
        self._resources = {}
        self._resources['all'] = {}
        self._config = {}
        self._config_file = ""

        # Recherche du fichier de configuration
        self._SetConfigFile(config_file)

        if self._config_file == "":
            print(f"Fichier de configuration non trouve [{config_file}]")
            exit()
        else:
            self._LoadConfig()
  
        # Creation des providers
        for my_provider in providers:
            self._resources[my_provider] = {}
            self.AddProvider(provider=my_provider)

    #
    # Protected methods
    #
    def _SetConfigFile(self, config_file:str):
        config_paths = [ # Liste des chemins ou chercher le fichier de configuration
            f"",
            f"./",
            f"{os.getcwd()}/",
            f"{os.getcwd()}/config/",
            f"{os.path.dirname(__file__)}/",
            f"{os.path.dirname(__file__)}/config/",
            ]

        for my_path in config_paths:
            if os.path.isfile(f"{my_path}{config_file}"):
                self._config_file = f"{my_path}{config_file}"
                break

    def _LoadConfig(self):
        try:
            config_file_mime_type = mimetypes.guess_type(self._config_file)[0]
            fp = open(self._config_file, "r")
            if config_file_mime_type == "application/json":
                try:
                    self._config = json.loads(fp.read())
                except Exception as e:
                    console.Print(f"Format json incorrect dans le fichier [{self._config_file}", "ERROR")
                    console.Print(e.__str__())
                    exit()
            else:
                console.Print(f"Format non pris en charge : {str(config_file_mime_type)}", "ERROR")
                exit()
            fp.close()
        except Exception as e:
            console.Print(f"Impossible de charger le fichier de configuration [{self._config_file}]","ERROR")
            console.Print(e.__str__())
            exit()

        if "inventory" in self._config:
            if "name" in self._config["inventory"]:
                self.name = self._config["inventory"]["name"]
            else:
                self.name = "Inventory"
            if "debug_mode" in self._config["inventory"]:
                console.SetDebugMode(self._config["inventory"]["debug_mode"])
            if "output" in self._config["inventory"]:
                if "mode" in self._config["inventory"]["output"]:
                    self._output_mode = self._config["inventory"]["output"]["mode"]
                if "format" in self._config["inventory"]["output"]:
                    self._output_format = self._config["inventory"]["output"]["format"]
                if "output_file" in self._config["inventory"]["output"]:
                    self._output_file = self._config["inventory"]["output"]["output_file"]

    #
    # Public methods
    #
    def AddProvider(self, provider: str=""):
        if provider == "aws":
            provider_config = {}
            if self._config_file != "":
                if "inventory" in self._config:
                    if "providers" in self._config["inventory"]:
                        if "aws" in self._config["inventory"]["providers"]:
                            provider_config = self._config["inventory"]["providers"]["aws"]
            from .aws.Aws import Aws
            self._providers[provider] = Aws(id="aws", name="AWS", config=provider_config)
        else:
            self._providers[provider] = Provider(id="unknown")

    def Data(self):
        datas = {}
        datas['configuration'] = self._config
        datas['resources'] = {}
        for my_resource_key, my_resource in self._resources['all'].items():
            if not my_resource.GetProperty('category') in datas['resources']:
                datas['resources'][my_resource.GetProperty('category')] = {}    
            datas['resources'][my_resource.GetProperty('category')][my_resource_key] = my_resource.Data()
        return datas

    def Id(self):
        return self._id

    def ListResources(self):
        for my_provider in self._providers.values():
            my_provider.ListResources()

    def LoadResources(self) -> dict:
        for my_provider_key, my_provider in self._providers.items():
            self._resources[my_provider_key] = my_provider.LoadResources()
            for resource_key, resource in self._resources[my_provider_key]['all'].items():
                self._resources['all'][resource_key] = resource
        return self._resources
    
    def Name(self):
        return self._name
    
    def Output(self):
        output = ""

        # Format de sortie
        if self._output_format == "json":
            output = self.ToJson()
        elif self._output_format == "table":
            output = self.ToTable()
        else:
            console.Print(text=f"Format de sortie non reconnu : {self._output_format}", text_format="ERROR")
            exit(1)

        # Mode de sortie
        if self._output_mode == "console":
            console.Print(output)
        elif self._output_mode =="file":
            output_file = open(self._output_file, "w")
            output_file.write(output)

        return output

    def Print(self):

        datas = []
        datas.append(["fichier de configuration", self._config_file])
        datas.append(["resources count", str(len(self._resources['all']))])
        console.PrintTab(title=f"{self.name}", datas=datas, footer="")

        for my_provider in self._providers.values():
            my_provider.Print()
            
    def PrintResources(self):
        for resource in self._resources['all'].values():
            resource.Print()

    def ToJson(self):
        json_output = json.dumps(self.Data(), indent=4, cls=CustomJSONEncoder)
        return json_output

    def ToTable(self) -> str:
        result = "["
        for my_resource in self._resources['all'].values():
            if result != "[":
                result += ","
            result += f"{my_resource.ToTable()}"
        result += "]"
        return result
