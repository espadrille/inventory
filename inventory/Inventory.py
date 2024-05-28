#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
import datetime
import json
import mimetypes
import os
from .Console import console
from .provider.Provider import Provider

#
# Classe d'inventaire
#
class Inventory:
    _name: str = ""
    _id: str = ""
    _config: dict
    _config_file: str
    _providers: dict
    _resources: dict
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id:str="", config_file :str=""):

        self._id = id
        self._name = ""

        self._output_format = "json"
        self._providers = {}
        self._resources = {}
        self._resources['all'] = {}
        self._config = {}
        self._config_file = ""
        self._summary = {}

        # Initialisation du resume
        self._summary['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Recherche du fichier de configuration
        self._SetConfigFile(config_file)

        if self._config_file == "":
            print(f"Fichier de configuration non trouve [{config_file}]")
            exit()
        else:
            self._LoadConfig()
  
        # Creation des providers
        for my_provider in self._providers:
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
        self._summary['config file'] = self._config_file

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

        if 'inventory' in self._config:
            if 'name' in self._config['inventory']:
                self.name = self._config['inventory']['name']
            else:
                self.name = 'inventory'

            if 'providers' in self._config['inventory']:
                for my_provider in self._config['inventory']['providers']:
                    self.AddProvider(my_provider)

            if 'debug_mode' in self._config['inventory']:
                console.SetDebugMode(self._config['inventory']['debug_mode'])

            if 'output' in self._config['inventory']:
                if not 'mode' in self._config['inventory']['output']:
                    self._config['inventory']['output']['mode'] = "console"
                if not 'format' in self._config['inventory']['output']:
                    self._config['inventory']['output']['format'] = "json"
                if not "output_file" in self._config['inventory']['output']:
                    self._config['inventory']['output']["output_file"] = ""

    #
    # Public methods
    #
    def AddProvider(self, provider: str=""):
        if provider == 'aws':
            provider_config = {}
            if self._config_file != "":
                if 'inventory' in self._config:
                    if 'providers' in self._config['inventory']:
                        if 'aws' in self._config['inventory']['providers']:
                            provider_config = self._config['inventory']['providers']['aws']
            from .aws.Aws import Aws
            self._providers[provider] = Aws(id='aws', name='aws', config=provider_config)
        else:
            self._providers[provider] = Provider(id="unknown")

    def Data(self):
        datas = {}
        datas['configuration'] = self._config
        datas['resources'] = {}
        for my_resource_key, my_resource in self._resources['all'].items():
            # Creer la 'category' la premiere fois uniquement
            if not my_resource.GetProperty('category') in datas['resources']:
                datas['resources'][my_resource.GetProperty('category')] = {}
            # Enregistrer la 'resource' dans sa 'category'
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
        self._summary['resource count'] = str(len(self._resources['all']))
        return self._resources
    
    def Name(self):
        return self._name
    
    def Write(self):
        # Choisir la bonne classe de formatteur
        if self._config['inventory']['output']['format'] == "json":
            from .output.JsonOutputFormatter import JsonOutputFormatter
            output_formatter = JsonOutputFormatter()
        elif self._config['inventory']['output']['format'] == "csv":
            from .output.CsvOutputFormatter import CsvOutputFormatter
            output_formatter = CsvOutputFormatter()
        elif self._config['inventory']['output']['format'] == "yaml":
            from .output.YamlOutputFormatter import YamlOutputFormatter
            output_formatter = YamlOutputFormatter()
        else:
            console.Print(text=f"Format de sortie non reconnu : {self._config['inventory']['output']['format']}", text_format="ERROR")
            from .output.OutputFormatter import OutputFormatter
            output_formatter = OutputFormatter()

        output_formatter.Init(config=self._config['inventory']['output'], resources=self._resources['all'])
        output_formatter.Write()

    def Print(self):
        datas = []
        for key, value in self._summary.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"{self.name}", datas=datas, footer="")

        for my_provider in self._providers.values():
            my_provider.Print()

    def ShowResources(self):
        for resource in self._resources['all'].values():
            resource.Print()

