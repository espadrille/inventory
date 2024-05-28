#
# classe OutputFormater
#
from ..Console import console
from ..Singleton import Singleton

class OutputFormatter(Singleton):
    _config: dict
    _resources: dict

    #
    # Private methods
    #
    def __init__(self):
        self._resources = {}
        self._config = {
            "mode": "console",
            "format": "text",
            "output_file": ""
        }

    #
    # Protected methods
    #
    def _select_fields(self):
        for my_resource_key, my_resource in self._resources.items():
            # Ne conserver que les champs selectionnes
            if len(self._config['selected_fields']) > 0:
                new_data = {}
                for my_field in self._config['selected_fields']:
                    if my_field in my_resource.Data().keys():
                        new_data[my_field] = my_resource.GetProperty(my_field)
                    else:
                        new_data[my_field] = ""
                self._resources[my_resource_key].Data(new_data)
            # print(my_resource.Data())

    def _LoadResources(self, resources:dict):
        self._resources = resources
        self._select_fields()

    def _LoadConfig(self, config:dict):
        self._config = config
        if not 'mode' in self._config:
            self._config['mode'] = 'console'
        if not 'format' in self._config:
            self._config['format'] = 'json'
        if not 'output_file' in self._config:
            self._config['output_file'] = ''
        if not 'selected_fields' in self._config:
            self._config['selected_fields'] = []
        if not 'csv_print_header' in self._config:
            self._config['csv_print_header'] = True
        if not 'csv_separator' in self._config:
            self._config['csv_separator'] = ','

    #
    # Public methods
    #
    def Init(self, config:dict, resources:dict):
        self._LoadConfig(config)
        self._LoadResources(resources)

    def Output(self):
        output = ""
        for resource_key, resource in self._resources.items():
            output += f"{resource_key}: {resource.Name()} - {resource.GetProperty('description')}\n"
        return output

    def Write(self):
        if self._config["mode"] == "console":
            console.Print(self.Output())
            console.Debug(f"Sortie affichee a la console")
        elif self._config["mode"] == "file":
            output_file = open(self._config["output_file"], "w")
            output_file.write(self.Output())
            console.Debug(f"Sortie ecrite dans le fichier {self._config['output_file']}")
            
