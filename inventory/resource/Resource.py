#
# Classe Resource
#
class Resource:
    _id: str
    _properties :dict
    _properties_mapping :dict = {}

    def __init__(self, id: str):
        self._id = id
        self._properties = {}
        self._properties['name'] = f"<{id}>"
        self._properties['description'] = ""

    def Id(self):
        return self._id

    def GetProperty(self, property_name :str):
        return self._properties[property_name]

    def SetProperty(self, property_name :str, property_value):
        self._properties[property_name] = property_value
        if property_name in self._properties_mapping.values():
            for my_mapping_key, my_mapping_value in self._properties_mapping.items():
                if my_mapping_value == property_name:
                    self._properties[my_mapping_key] = property_value

    def print(self):
        print(f"{self._id}:")
        for my_property_key, my_property in dict(sorted(self._properties.items())).items():
            print(f"    {my_property_key} : {my_property}")

