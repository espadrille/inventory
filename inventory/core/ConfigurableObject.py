'''
    ConfigurableObject
'''

import json
import mimetypes
import os
import sys
import boto3
from ..core.Console import console
from ..core.Object import Object

class ConfigurableObject(Object):
    '''
        Classe : ConfigurableObject
        Ajoute la propriete self._config:dict() a un objet, et quelques fonctions de gestion
    '''
    _config: dict

    def __init__(self, config:dict=None, config_source :str="") -> None:
        if config is None:
            config = {}

        super().__init__()
        self._config = config

        # Chargement de la configuration
        if config != {}:
            self.SetProperty('configuration', 'inline')
            self._load_config(config)
        if config_source != "":
            self.SetProperty('configuration', config_source)
            if config_source.startswith('ssm:') :
                self._load_config_from_ssm(config_source[4:])
            else:
                self._load_config_from_file(config_source)


    def _complete_config(self, config:dict, default_config: dict) -> dict:
        # Completer recursivement les elements de configuration manquants par des valeurs par defaut
        new_config = config
        for k, v in default_config.items():
            if k in config:
                if isinstance(v, dict):
                    new_config[k] = self._complete_config(config[k], v)
                else:
                    new_config[k] = config[k]
            else:
                new_config[k] = v
        return new_config

    def _load_config(self, config:dict):
        self._config = config


    def _load_config_from_file(self, config_file:str) -> None:
        config_paths = [ # Liste des chemins ou chercher le fichier de configuration
            "",
            "./",
            f"{os.getcwd()}/",
            f"{os.getcwd()}/config/",
            f"{os.path.dirname(__file__)}/",
            f"{os.path.dirname(__file__)}/config/",
            f"{os.path.dirname(__file__)}/../config/"
            ]

        my_config_file = ""
        for my_path in config_paths:
            if os.path.isfile(f"{my_path}{config_file}"):
                my_config_file = f"{my_path}{config_file}"
                self.SetProperty('configuration', my_config_file)
                break

        try:
            config_file_mime_type = mimetypes.guess_type(my_config_file)[0]
            with open(my_config_file, "r", encoding='utf-8') as fp:
                if config_file_mime_type == "application/json":
                    try:
                        str_config = fp.read()
                        self._load_config(json.loads(str_config))
                    except Exception as e:
                        console.Print(f"Format json incorrect dans le fichier [{config_file}]", "ERROR")
                        console.Print(str(e))
                        sys.exit(1)
                else:
                    console.Print(f"Format non pris en charge : {str(config_file_mime_type)}", "ERROR")
                    sys.exit(1)
        except Exception as e:
            console.Print(f"Impossible de charger le fichier de configuration [{config_file}]","ERROR")
            console.Print(str(e))
            sys.exit(1)


    def _load_config_from_ssm(self, ssm_parameter:str) -> None:
        try:
            ssm = boto3.Session().client(service_name='ssm')
            str_config = ssm.get_parameter(Name=ssm_parameter, WithDecryption=True)['Parameter']['Value']
            self._load_config(json.loads(str_config))
        except Exception as e:
            console.Print(f"Le parametre {ssm_parameter} n'a pas pu etre lu dans SSM Parameter Store.","ERROR")
            console.Print(str(e))


    def _get_config_value(self, config_key:str) -> str:
        if config_key.startswith('ssm:') :
            return self._get_config_value_from_ssm(config_key[4:])
        return self._config[config_key]

    def _get_config_value_from_ssm(self, ssm_parameter:str) -> str:
        try:
            ssm = boto3.Session().client(service_name='ssm')
            return ssm.get_parameter(Name=ssm_parameter, WithDecryption=True)['Parameter']['Value']
        except Exception as e:
            console.Print(f"Le parametre {ssm_parameter} n'a pas pu etre lu dans SSM Parameter Store.","ERROR")
            console.Print(str(e))
            return ""
