#
# Generation d'inventaires d'infrastructure
#

#
# Imports
#
import datetime
from .Console import console
from .provider.Provider import Provider
from .ConfigurableObject import ConfigurableObject

#
# Classe d'inventaire
#
class Inventory(ConfigurableObject):
    _providers: dict
    _resources: dict
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, id:str="", config_source :str="", colorize :bool=True):
        super().__init__(config_source=config_source)

        console.SetColorize(colorize)

        self.SetProperty('Id', id)

        self._providers = {}
        self._resources = {}
        self._resources['all'] = {}
        self._summary = {}

        # Initialisation du resume
        self._summary['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._summary['configuration'] = self.GetProperty('configuration')
        self._parse_config()
        self.SetProperty('Name', self._config['inventory']['name'])
  
        # Creation des providers
        for my_provider in self._providers:
            self._resources[my_provider] = {}
            self.AddProvider(provider=my_provider)

    #
    # Protected methods
    #

    def _parse_config(self):
        
        # Completer les valeurs manquantes de self._config avec les valeur par defaut
        self._config = self._complete_config(config=self._config, default_config={
            'inventory': {
                'name': 'inventory',
                'providers': {
                    },
                'debug_mode': '',
                'output': {
                    'mode': 'console',
                    'format': 'json'
                    }
                }
            })

        for my_provider in self._config['inventory']['providers']:
            self.AddProvider(my_provider)

        console.SetDebugMode(self._config['inventory']['debug_mode'])

        self._summary['output'] = self._config['inventory']['output']['mode']
        if self._config['inventory']['output']['mode'] == "file":
            self._summary['output file'] = self._config['inventory']['output']['output_file']

    #
    # Public methods
    #
    def AddProvider(self, provider: str=""):
        if provider == 'aws':
            from .aws.Aws import Aws
            self._providers[provider] = Aws(id='aws', name='aws', config=self._config['inventory']['providers']['aws'])
        elif provider == 'vsphere':
            from .vsphere.Vsphere import Vsphere
            self._providers[provider] = Vsphere(id='vsphere', name='vsphere', config=self._config['inventory']['providers']['vsphere'])
        else:
            self._providers[provider] = Provider(id="unknown")

    def Data(self):
        datas = {}
        datas['configuration'] = self._config
        datas['resources'] = {}
        for my_resource_key, my_resource in self._resources['all'].items():
            # Creer la 'category' la premiere fois uniquement
            if not my_resource.GetProperty('Category') in datas['resources']:
                datas['resources'][my_resource.GetProperty('Category')] = {}
            # Enregistrer la 'resource' dans sa 'category'
            datas['resources'][my_resource.GetProperty('Category')][my_resource_key] = my_resource.Data()
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
        return self.GetProperty('Name')
    
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
        console.PrintTab(title=f"{self.GetProperty('Name')}", datas=datas, footer="", text_format="GREEN")

        for my_provider in self._providers.values():
            my_provider.Print()

    def ShowResources(self):
        for resource in self._resources['all'].values():
            resource.Print()

