from ..Console import console
from ..resource.Resource import Resource

class VsphereResource(Resource):
    '''
        Classe VsphereResource
    '''

    _arn: str
    _tags: list=[]

    #
    # Private methods
    #
    def __init__(self, category: str, id: str, resource: dict):
        super().__init__(category=f"vsphere.{category}", id=f"{id}")
        for my_property_key in dir(resource):
            try:
                self.SetProperty(my_property_key, getattr(resource, my_property_key))
            except Exception:
                pass

        # Tenter de lire les tags s'il y en a...
        if self._get_tag_value('Name') != "":
            self.SetProperty('Name', self._get_tag_value('Name'))
        if self._get_tag_value('Description') != "":
            self.SetProperty('Description', self._get_tag_value('Description'))

    #
    # Protected methods
    #
    def _get_tags(self) -> list:
        return self._tags

    def _get_tag_value(self, tag_name: str) -> str:
        result = ""
        for my_tag in self._tags:
            if my_tag['Key'] == tag_name:
                result = my_tag['Value']
        return result