'''
    Resource
'''

# Imports
import datetime
import json
import time
from ..core.Console import console
from ..core.CustomJSONEncoder import CustomJSONEncoder
from ..core.Object import Object

#
# Classe Resource
#
class Resource(Object):
    '''
        Classe Resource
    '''

    _properties_mapping :dict = {}

    #
    # Private methods
    #
    def __init__(self, category:str, id: str) -> None:
        '''
            Initialiseur de la clase
        '''

        super().__init__()
        self.SetProperty('id', id)
        self.SetProperty('Name', f"<{id}>")
        self.SetProperty('Description', "")
        self.SetProperty('Category', category)
        self.SetProperty('Date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __str__(self) -> str:
        return self.ToJson()

    #
    # Protected methods
    #
    def _execute_with_retry(self, func, *args, max_retries=7, initial_delay=1):
        '''
            Executer une fonction/methode et re_essayer {max_retries} fois avant d'echouer.
            Le delai entre deux executions est augmente apres chaque tentative.
        '''
        retries = 0
        delay = initial_delay
        while retries < max_retries:
            try:
                return func(*args)
            except Exception:
                retries += 1
                console.Debug(f"{self.GetProperty('Name')} : Erreur lors de l'execution de {func.__name__}: Re-essai {retries}/{max_retries} dans {delay} secondes.")
                time.sleep(delay)
                delay *= 2  # Backoff exponentiel
        console.Debug(f"{self.GetProperty('Name')} : Echec de {func.__name__} aprés {max_retries} tentatives.")
        # raise Exception(f"Echec de {func.__name__} aprés {max_retries} tentatives.")

    #
    # Public methods
    #
    def Data(self, new_data: dict=None) -> dict:
        '''
            Retourne les proprietes de la ressource
        '''

        if new_data is not None:
            self.SetProperties(new_data)
        return self.GetProperties()

    def Description(self):
        '''
            Retourne la description de la ressource
        '''

        return self.GetProperty('Description')

    def Id(self) -> str:
        '''
            Retourne l'identifiant de la ressource
        '''

        return self.GetProperty('id')

    def InventoryId(self):
        '''
            Retourne l'identifiant de l'inventaire proprietaire de la ressource
        '''

        return f"{self.GetProperty('Category')}.{self.GetProperty('id')}"

    def Name(self):
        '''
            Retourne le nom de la ressource
        '''

        return self.GetProperty('Name')

    def Print(self):
        '''
            Affiche la ressource
        '''

        console.Print(self.ToJson())

    def SetProperty(self, property_name :str, property_value):
        '''
            Change la valeur d'une propriete de la ressource
        '''

        super().SetProperty(property_name, property_value)
        if property_name in self._properties_mapping.values():
            for my_mapping_key, my_mapping_value in self._properties_mapping.items():
                if my_mapping_value == property_name:
                    super().SetProperty(my_mapping_key, property_value)

    def ToJson(self):
        '''
            Serialise la ressource en JSON
        '''

        json_output = json.dumps(self.Data(), indent=4, cls=CustomJSONEncoder)
        return json_output

    def ToTable(self):
        '''
            Retourne un tableau des proprietes de la ressource
        '''

        datas = []
        for key, value in self.GetProperties().items():
            datas.append([key, str(value)])
        return datas
