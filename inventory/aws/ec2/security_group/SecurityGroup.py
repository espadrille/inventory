# Instance EC2

#
# Imports
#
import boto3
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

#
# Classe Instance
#
class SecurityGroup(AwsResource):
    _client : AwsClient
    _properties_mapping = {
        'id': 'GroupId'
        }

    #
    # Private methods
    #
    def __init__(self, security_group: dict, client: AwsClient):
        self._client = client
        super().__init__(category=f"ec2.security_group", id=f"{security_group['GroupId']}", object=security_group)

        self.SetProperty('account_id', client.Client().describe_security_groups()['SecurityGroups'][0]['OwnerId'])
        self.SetProperty('region', client.Client()._client_config._user_provided_options['region_name'])
        self.SetProperty('arn', f"arn:aws:ec2:{self.GetProperty('region')}:{self.GetProperty('account_id')}:security-group/{self.Id()}")

    #
    # Protected methods
    #
    def _get_tags(self):
        Tags :list
        try:
            Tags = self._client.Client().describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('id')]}])['Tags']
        except:
            Tags = []
        return Tags
        
