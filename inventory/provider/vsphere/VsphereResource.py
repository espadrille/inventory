'''
    Module de classe VsphereResource
'''

from ...core.Resource import Resource

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
        '''
            Constructeur de classe
        '''
        super().__init__(category=f"vsphere.{category}", id=f"{id}")
        #
        # Recuperer uniquement les proprietes serialisables, et pas les methodes
        #
        for my_property_key in dir(resource):
            if callable(getattr(resource, my_property_key, None)):
                # Eviter les methodes
                continue
            try:
                value = getattr(resource, my_property_key)
                if isinstance(value, (str, int, float, list, dict, bool, type(None))):
                    # Eviter les types non serialisables
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
        '''
            Retourne les tags de la ressource
        '''
        return self._tags

    def _get_tag_value(self, tag_name: str) -> str:
        '''
            Retourne la valeur d'un tag donne
        '''
        result = ""
        for my_tag in self._tags:
            if my_tag['Key'] == tag_name:
                result = my_tag['Value']
        return result
