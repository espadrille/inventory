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
        'Id': 'InstanceId'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: AwsClient):
        self._client = client
        super().__init__(category=f"ec2.instance", id=f"{instance['InstanceId']}", object=instance)

        self.SetProperty('AccountId', client.Client().describe_instances()['Reservations'][0]['OwnerId'])
        self.SetProperty('Region', client.Region())
        self.SetProperty('Arn', f"arn:aws:ec2:{self.GetProperty('Region')}:{self.GetProperty('AccountId')}:instance/{self.Id()}")
        self.SetProperty('State', instance['State']['Name'])
        self.SetProperty('StateCode', int(instance['State']['Code']))

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('AWS.[A-Z]{1,2}([0-9]{2,3})', self._properties['Name'])
        if result:
            self.SetProperty('Increment', int(result.group(1)))
        else:
            # Nouvelle convetion de nommage
            result = re.match('aws[a-z0-9]{5}([0-9]{3})', self._properties['Name'])
            if result:
                self.SetProperty('Increment', int(result.group(1)))
            else:
                self.SetProperty('Increment', 0)

    #
    # Protected methods
    #
    def _get_tags(self):
        Tags :list
        try:
            Tags = self._client.Client().describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('Id')]}])['Tags']
        except:
            Tags = []
        return Tags
        
