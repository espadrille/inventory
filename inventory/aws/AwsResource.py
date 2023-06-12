#
# Classe AwsResource
#
import boto3
from ..resource.Resource import Resource

class AwsResource(Resource):
    _client :boto3.client.__class__

    #
    # Private methods
    #
    def __init__(self, id: str, client: boto3.client.__class__, object: dict):
        super().__init__(id=f"aws.{id}")
        self._client = client

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

    #
    # Public methods
    #
    def Id(self):
        return self._id
    