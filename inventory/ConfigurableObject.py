#
# Classe : ConfigurableObject
# Ajoute la propriete self._config:dict() a un objet, et quelques fonctions de gestion
#
class ConfigurableObject():
    _config: dict

    def __init__(self):
        self._config = {}

    def _complete_config(self, config:dict, default_config: dict):
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
