'''
    CsvOutputFormater
'''

from ..Console import console
from .OutputFormatter import OutputFormatter

class CsvOutputFormatter(OutputFormatter):
    '''
        Classe CsvOutputFormater
    '''

    def Output(self):
        console.Debug("Preparation de la sortie au format CSV...")
        # Conversion de la liste d'objets en csv:
        printed_headers = False
        if not self._config['csv_print_header']:
            printed_headers = True

        output = ""
        for resource_key, resource in self._resources.items():
            if not printed_headers:
                header_line = ""
                for my_field_key, my_field_value in resource.Data().items():
                    if header_line != "":
                        header_line += self._config['csv_separator']
                    header_line += f"\"{my_field_key}\""
                output += f"{header_line}\n"
                printed_headers = True
            resource_line = ""
            for my_field_key, my_field_value in resource.Data().items():
                if resource_line != "":
                    resource_line += self._config['csv_separator']
                resource_line += f"\"{my_field_value}\""
            output += f"{resource_line}\n"
            
        return output
