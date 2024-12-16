'''
    Security group
'''
#
# Imports
#
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

class SecurityGroup(AwsResource):
    '''
        Classe SecurityGroup
    '''

    _client : AwsClient
    _properties_mapping = {
        'Id': 'GroupId'
        }

    #
    # Private methods
    #
    def __init__(self, security_group: dict, client: AwsClient):
        self._client = client
        self._tags = []
        super().__init__(category="ec2.security_group", id=f"{security_group['GroupId']}", object=security_group)

        self.SetProperty('AccountId', client.Client().describe_security_groups()['SecurityGroups'][0]['OwnerId'])
        self.SetProperty('Region', client.Client()._client_config._user_provided_options['region_name'])
        self.SetProperty('Arn', f"arn:aws:ec2:{self.GetProperty('Region')}:{self.GetProperty('AccountId')}:security-group/{self.Id()}")

    #
    # Protected methods
    #
    def _get_tags(self):
        try:
            self._tags = self._client.Client().describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('Id')]}])['Tags']
        except Exception:
            self._tags = []
        return self._tags
