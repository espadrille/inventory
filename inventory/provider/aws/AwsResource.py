'''
    Module de classe AwsResource
'''

from ...core.Resource import Resource

class AwsResource(Resource):
    '''
        Classe AwsResource
    '''

    _arn: str
    _tags: list=[]

    #
    # Private methods
    #
    def __init__(self, category: str, id: str, object: dict):
        '''
            Constructeur de la classe
        '''

        super().__init__(category=f"aws.{category}", id=f"{id}")

        for my_property_key, my_property_value in object.items():
            self.SetProperty(my_property_key, my_property_value)

        # Tenter de lire les tags s'il y en a...
        if len(self._get_tags()) > 0 :
            if self._get_tag_value('Name') != "":
                self.SetProperty('Name', self._get_tag_value('Name'))
            if self._get_tag_value('Description') != "":
                self.SetProperty('Description', self._get_tag_value('Description'))
            if self._get_tag_value('TerraformRoot') != "":
                self.SetProperty('TerraformRoot', self._get_tag_value('terraform_root'))
            if self._get_tag_value('TerraformModule') != "":
                self.SetProperty('TerraformModule', self._get_tag_value('terraform_module'))

    #
    # Protected methods
    #
    def _init_tags(self, tags_list:list=None):
        '''
            Initilase la liste de tags
        '''
        if tags_list is None:
            self._tags = []
        else:
            self._tags = tags_list

    def _get_tags(self) -> list:
        '''
            Retourne les tags
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
