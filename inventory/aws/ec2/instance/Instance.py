# Instance EC2

#
# Imports
#
import re
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

#
# Classe Instance
#
class Instance(AwsResource):
    _client : AwsClient
    _properties_mapping = {
        'id': 'InstanceId'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: AwsClient):
        self._client = client
        super().__init__(category=f"ec2.instance", id=f"{instance['InstanceId']}", object=instance)

        self.SetProperty('account_id', client.Client().describe_instances()['Reservations'][0]['OwnerId'])
        self.SetProperty('region', client.Region())
        self.SetProperty('arn', f"arn:aws:ec2:{self.GetProperty('region')}:{self.GetProperty('account_id')}:instance/{self.Id()}")
        self.SetProperty('state', instance['State']['Name'])
        self.SetProperty('state_code', int(instance['State']['Code']))

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('AWS.[A-Z]{1,2}([0-9]{2,3})', self._properties['name'])
        if result:
            self.SetProperty('increment', int(result.group(1)))
        else:
            self.SetProperty('increment', 0)

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
        
