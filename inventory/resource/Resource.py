# Imports
import datetime
import json
from ..Console import console
from ..CustomJSONEncoder import CustomJSONEncoder

#
# Classe Resource
#
class Resource:
    _id: str
    _properties :dict
    _properties_mapping :dict = {}

    #
    # Private methods
    #
    def __init__(self, category:str, id: str):
        self._id = id
        self._properties = {}
        self._properties['name'] = f"<{id}>"
        self._properties['description'] = ""
        self._properties['category'] = category
        self._properties['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return self.ToJson()

    #
    # Public methods
    #
    def Data(self, new_data: dict={}):
        if new_data != {}:
            self._properties = new_data
        return self._properties

    def Description(self):
        return self._properties['description']

    def GetProperty(self, property_name :str):
        try:
            return self._properties[property_name]
        except:
            return ""
    
    def Id(self):
        return self._id
    
    def InventoryId(self):
        return f"{self.GetProperty('category')}.{self._id}"
    
    def Name(self):
        return self.GetProperty('name')

    def Print(self):
        datas = []
        for key, value in self._properties.items():
            datas.append([key, str(value)])
        console.PrintTab(title=f"Resource {self.Name()}", datas=datas, footer="")

    def SetProperty(self, property_name :str, property_value):
        self._properties[property_name] = property_value
        if property_name in self._properties_mapping.values():
            for my_mapping_key, my_mapping_value in self._properties_mapping.items():
                if my_mapping_value == property_name:
                    self._properties[my_mapping_key] = property_value

    def ToJson(self):
        json_output = json.dumps(self.Data(), indent=4, cls=CustomJSONEncoder)
        return json_output

    def ToTable(self):
        datas = []
        for key, value in self._properties.items():
            datas.append([key, str(value)])
        return datas

