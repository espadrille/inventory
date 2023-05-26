# Instance EC2

#
# Imports
#
import boto3
from ...AwsResource import AwsResource

#
# Classe Instance
#
class SecurityGroup(AwsResource):
    _properties_mapping = {
        'id': 'GroupId'
        }

    def __init__(self, security_group: dict, client: boto3.client.__class__):
        super().__init__(id=f"ec2.security-group.{security_group['GroupId']}", object=security_group, client=client)

    def _get_tags(self):
        Tags :list
        try:
            Tags = self._client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('id')]}])['Tags']
        except:
            Tags = []
        return Tags
        
