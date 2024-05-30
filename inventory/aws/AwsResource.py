#
# Classe AwsResource
#
from ..resource.Resource import Resource

class AwsResource(Resource):
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
        self._get_tags()
        self.SetProperty('Name', self._get_tag_value('Name'))
        self.SetProperty('Description', self._get_tag_value('Description'))
        self.SetProperty('TerraformRoot', self._get_tag_value('terraform_root'))
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