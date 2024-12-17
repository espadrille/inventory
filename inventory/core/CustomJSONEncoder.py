import json
from datetime import datetime

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False
    
class CustomJSONEncoder(json.JSONEncoder):
    '''
        Classe CustomJSONEncoder
    '''
    visited: set

    def __init__(self, *args, **kwargs):
        self.visited = set()  # Ensemble pour suivre les objets déjà sérialisés
        super().__init__(*args, **kwargs)

    def default(self, o):
         
        if is_json_serializable(o):
            return o

        # Gestion des objets datetime
        if isinstance(o, datetime):
            return o.isoformat()

        # Gestion des objets de type 'set'
        if isinstance(o, set):
            return list(o)

        # Gestion des objets personnalisés avec '__dict__'
        if hasattr(o, '__dict__'):
            obj_id = id(o)
            if obj_id in self.visited:
                return f"<CircularReference: {type(o).__name__}>"
            self.visited.add(obj_id)
            try:
                # Sérialiser seulement les attributs publics non appelables
                return {
                    k: self.default(v)
                    for k, v in o.__dict__.items()
                    if not k.startswith('_') and not callable(v)
                }
            except Exception:
                return f"<Unserializable: {str(o)}>"

        # Par défaut, appeler le comportement de la superclasse
        return super().default(o)

