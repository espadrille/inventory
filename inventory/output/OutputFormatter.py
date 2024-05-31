#
# classe OutputFormater
#
import boto3
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
                for my_field_key, my_field in self._config['selected_fields'].items():
                    if my_field_key in my_resource.Data().keys():
                        new_data[my_field] = my_resource.GetProperty(my_field_key)
                    else:
                        new_data[my_field] = ""
                self._resources[my_resource_key].Data(new_data)
            # print(my_resource.Data())

    def _LoadResources(self, resources:dict):
        self._resources = resources
        self._select_fields()

    def _completeConfig(self, config:dict, default_config: dict):
        # Completer recursivement les elements de configuration manquants
        for k, v in default_config.items():
            if not k in config:
                config[k] = v
            if isinstance(v, dict):
                config[k] = self._completeConfig(config[k], v)
                
        return config

    def _LoadConfig(self, config:dict):
        default_config = {
            'mode': 'console',
            'format': 'json',
            'output_file': '',
            'selected_fields': [],
            'csv_print_header': True,
            'csv_separator': ','
            }
        
        # Completer les valeurs manquantes de config avec les valeur par defaut
        self._config = self._completeConfig(config, default_config)

        if self._config['mode'] == 'file':
            if self._config['output_file'].startswith('s3:'):
                separated_string = self._config['output_file'][3:].split('/')
                self._config['s3_bucketname'] = separated_string[0]
                self._config['s3_key'] = '/'.join(separated_string[1:])
        if self._config['mode'] == 'json':
            self._config['output_mimetype'] = 'application/json'
        else:
            self._config['output_mimetype'] = 'text/plain'

    #
    # Public methods
    #
    def Init(self, config:dict, resources:dict):
        self._LoadConfig(config)
        self._LoadResources(resources)

    def Output(self):
        output = ""
        for resource_key, resource in self._resources.items():
            resource_line = ""
            for my_field_key, my_field_value in resource.Data().items():
                if resource_line != "":
                    resource_line += ','
                resource_line += f"{my_field_key}=\"{my_field_value}\""
            output += f"{resource_line}\n"
        return output

    def Write(self):
        if self._config['mode'] == 'console':
            console.Print(self.Output())
            console.Debug(f"Sortie affichee a la console")
        elif self._config['mode'] == 'file':
            if self._config['output_file'].startswith('s3:'):
                s3 = boto3.Session().client(service_name='s3')
                try:
                    s3.put_object(
                        Bucket=self._config['s3_bucketname'], 
                        Key=self._config['s3_key'], 
                        ContentType=self._config['output_mimetype'],
                        Body=self.Output()
                        )
                except Exception as e:
                    console.Print(f"Le fichier {self._config['output_file']} n'a pas pu etre ecrit dans S3.","ERROR")
                    console.Print(e.__str__())
            else:
                output_file = open(self._config['output_file'], 'w')
                output_file.write(self.Output())
                console.Debug(f"Sortie ecrite dans le fichier {self._config['output_file']}")
            