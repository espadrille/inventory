'''
    OutputFormater
'''

import yaml
from ..core.Console import console
from .OutputFormatter import OutputFormatter

class YamlOutputFormatter(OutputFormatter):
    '''
        Classe OutputFormater
    '''


    def Output(self):
        console.Debug("Preparation de la sortie au format YAML...")
        # Conversion de la liste d'objets en dict:
        my_resources: dict = {}
        for resource_key, resource in self._resources.items():
            my_resources[resource_key] = resource.Data()

        # Format de sortie en yaml
        output = yaml.dump(my_resources)

        return output
