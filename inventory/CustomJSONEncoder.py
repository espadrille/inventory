'''
    Serialisation d'un objet en JSON
'''
# Imports
import datetime
from json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        # Gestion des objets datetime
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, datetime.time):
            return o.isoformat()

        # Gestion des objets de type `set`
        if isinstance(o, set):
            return list(o)

        # Gestion des objets personnalisés avec `__dict__`
        if hasattr(o, '__dict__'):
            try:
                # Sérialiser seulement les attributs publics
                return {k: v for k, v in o.__dict__.items() if not k.startswith('_')}
            except Exception:
                return str(o)

        # Par défaut, appeler le comportement de la superclasse
        return super().default(o)
