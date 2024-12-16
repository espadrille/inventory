'''
    OutputFormater
'''

import json
from ..core.Console import console
from ..core.CustomJSONEncoder import CustomJSONEncoder
from .OutputFormatter import OutputFormatter

class JsonOutputFormatter(OutputFormatter):
    '''
        Classe OutputFormater
    '''

    def Output(self):
        console.Debug("Preparation de la sortie au format JSON...")
        # Conversion de la liste d'objets en dict:
        my_resources: dict = {}
        for resource_key, resource in self._resources.items():
            my_resources[resource_key] = resource.Data()

        # Format de sortie en json
        output = json.dumps(my_resources, indent=4, cls=CustomJSONEncoder)

        return output
