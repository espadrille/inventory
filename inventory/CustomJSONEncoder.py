
# Imports
import datetime
from json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o)
        if hasattr(o, '__dict__'):
            try:
                return o.__dict__
            except Exception:
                return {k: v for k, v in o.__dict__.items() if not k.startswith('_')}
