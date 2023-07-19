
# Imports
import datetime
from json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return f"{o}"
        else:
            return o.__dict__

