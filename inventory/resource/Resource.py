# Imports
import datetime
import json
import time
from ..Console import console
from ..CustomJSONEncoder import CustomJSONEncoder
from ..Object import Object

#
# Classe Resource
#
class Resource(Object):
    _properties_mapping :dict = {}

    #
    # Private methods
    #
    def __init__(self, category:str, id: str) -> None:
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
            except Exception as e:
                retries += 1
                console.Debug(f"Erreur lors de l'exécution de {func.__name__}: Réessai {retries}/{max_retries} dans {delay} secondes.")
                time.sleep(delay)
                delay *= 2  # Backoff exponentiel
        raise Exception(f"Échec de {func.__name__} après {max_retries} tentatives.")

    #
    # Public methods
    #
    def Data(self, new_data: dict={}) -> dict:
        if new_data != {}:
            self.SetProperties(new_data)
        return self.GetProperties()

    def Description(self):
        return self.GetProperty('Description')
    
    def Id(self) -> str:
        return self.GetProperty('id')
    
    def InventoryId(self):
        return f"{self.GetProperty('Category')}.{self.GetProperty('id')}"
    
    def Name(self):
        return self.GetProperty('Name')

    def Print(self):
        console.Print(self.ToJson())

    def SetProperty(self, property_name :str, property_value):
        super().SetProperty(property_name, property_value)
        if property_name in self._properties_mapping.values():
            for my_mapping_key, my_mapping_value in self._properties_mapping.items():
                if my_mapping_value == property_name:
                    super().SetProperty(my_mapping_key, property_value)

    def ToJson(self):
        json_output = json.dumps(self.Data(), indent=4, cls=CustomJSONEncoder)
        return json_output

    def ToTable(self):
        datas = []
        for key, value in self.GetProperties().items():
            datas.append([key, str(value)])
        return datas

