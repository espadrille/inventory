#
# Classe Resource
#
import boto3
from ..resource.Resource import Resource

class AwsResource(Resource):
    profile :str
    _client :boto3.client.__class__
    terraform_module :str
    terraform_root :str
    arn :str

    def __init__(self, id: str, client: boto3.client.__class__, name: str="", arn :str=""):
        super().__init__(id=id, name=name)
        self._client = client
        self.terraform_module = ""
        self.terraform_root = ""
        self.arn = arn

        # Tenter de lire les tags s'il y en a...
        for tag in self._get_tags(client=client):
            if tag['Key'] == 'Name':
                self.name = tag['Value']
            if tag['Key'] == 'Description':
                self.description = tag['Value']
            if tag['Key'] in ['terraform_root', 'terraform_project']:
                self.terraform_root = tag['Value']
            if tag['Key'] == 'terraform_module':
                self.terraform_module = tag['Value']
        
    def print(self):
        super().print()
        print(f"    profile             : {self.profile}")
        if self.terraform_module != "":
            print(f"    terraform_module    : {self.terraform_module}")
        if self.terraform_root != "":
            print(f"    terraform_root      : {self.terraform_root}")

    def _get_tags(self, client: boto3.client.__class__):
        return []