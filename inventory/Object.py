'''
    Objet
'''
from .Console import console

class Object(object):
    '''
        Classe : Object
        Classe de base pour tous les objets
    '''

    _properties: dict

    def __init__(self) -> None:
        self._properties = {}


    def GetProperty(self, property_name :str):
        '''
            Obtenir une propriete de l'objet
        '''

        try:
            return self._properties[property_name]
        except Exception as e:
            console.Print(str(e))
            return ""


    def SetProperty(self, property_name :str, property_value):
        '''
            Definir une propriete de l'objet
        '''

        self._properties[property_name] = property_value


    def GetProperties(self) -> dict:
        '''
            Obtenir toutes les proprietes de l'objet
        '''

        return self._properties


    def SetProperties(self, properties: dict) -> dict:
        '''
            Definir toutes les proprietes de l'objet
        '''

        self._properties = properties
    