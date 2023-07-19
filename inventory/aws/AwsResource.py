#
# Classe AwsResource
#
from ..resource.Resource import Resource

class AwsResource(Resource):
    _arn: str

    #
    # Private methods
    #
    def __init__(self, category: str, id: str, object: dict):
        super().__init__(category=f"aws.{category}", id=f"{id}")

        for my_property_key, my_property_value in object.items():
            self.SetProperty(my_property_key, my_property_value)

        # Tenter de lire les tags s'il y en a...
        for tag in self._get_tags():
            if tag['Key'] == 'Name':
                self.SetProperty('name', tag['Value'])
            if tag['Key'] == 'Description':
                self.SetProperty('description', tag['Value'])
            if tag['Key'] in ['terraform_root', 'terraform_project']:
                self.SetProperty('terraform_root', tag['Value'])
            if tag['Key'] == 'terraform_module':
                self.SetProperty('terraform_module', tag['Value'])

    #
    # Protected methods
    #
    def _get_tags(self) -> list:
        return []

