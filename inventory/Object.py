#
# Classe : Object
# Classe de base pour tous les objets
#

class Object():
    _properties: dict

    def __init__(self) -> None:
        self._properties = {}


    def GetProperty(self, property_name :str):
        try:
            return self._properties[property_name]
        except:
            return ""


    def SetProperty(self, property_name :str, property_value):
        self._properties[property_name] = property_value


    def GetProperties(self) -> dict:
        return self._properties


    def SetProperties(self, properties: dict) -> dict:
        self._properties = properties
    