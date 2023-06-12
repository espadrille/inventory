# Instance EC2

#
# Imports
#
import boto3
import re
from ...AwsResource import AwsResource

#
# Classe Instance
#
class Instance(AwsResource):
    _properties_mapping = {
        'id': 'InstanceId'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: boto3.client.__class__):
        super().__init__(id=f"ec2.instance.{instance['InstanceId']}", client=client, object=instance)
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
            Tags = self._client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('id')]}])['Tags']
        except:
            Tags = []
        return Tags
        
