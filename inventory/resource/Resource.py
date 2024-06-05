# Imports
import datetime
import json
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

