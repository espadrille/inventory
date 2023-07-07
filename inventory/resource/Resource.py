# Imports
from ..Console import console

#
# Classe Resource
#
class Resource:
    _category: str
    _id: str
    _properties :dict
    _properties_mapping :dict = {}

    #
    # Private methods
    #
    def __init__(self, category:str, id: str):
        self._category = category
        self._id = id
        self._properties = {}
        self._properties['name'] = f"<{id}>"
        self._properties['description'] = ""

    #
    # Public methods
    #
    def Description(self):
        return self._properties['description']

    def GetProperty(self, property_name :str):
        return self._properties[property_name]
    
    def Id(self):
        return self._id
    
    def InventoryId(self):
        return f"{self._category}.{self._id}"
    
    def Name(self):
        return self._properties['name']

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

