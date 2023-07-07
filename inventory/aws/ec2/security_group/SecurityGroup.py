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

    #
    # Private methods
    #
    def __init__(self, security_group: dict, client: boto3.client.__class__):
        super().__init__(category=f"ec2.security-group", id=f"{security_group['GroupId']}", object=security_group, client=client)

        self.SetProperty('account_id', client.describe_security_groups()['SecurityGroups'][0]['OwnerId'])
        self.SetProperty('region', client._client_config._user_provided_options['region_name'])
        self.SetProperty('arn', f"arn:aws:ec2:{self.GetProperty('region')}:{self.GetProperty('account_id')}:security-group/{self.Id()}")

    #
    # Protected methods
    #
    def _get_tags(self):
        Tags :list
        try:
            Tags = self._client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('id')]}])['Tags']
        except:
            Tags = []
        return Tags
        
