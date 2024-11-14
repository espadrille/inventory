from ..resource.Resource import Resource

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
    def _get_tags(self) -> list:
        return self._tags

    def _get_tag_value(self, tag_name: str) -> str:
        result = ""
        for my_tag in self._tags:
            if my_tag['Key'] == tag_name:
                result = my_tag['Value']
        return result