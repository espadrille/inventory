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
    type :str
    state :str
    state_code :int
    increment :int

    def __init__(self, instance: dict, client: boto3.client.__class__):
        super().__init__(id=instance['InstanceId'], name=instance['InstanceId'], client=client)
        self.type = instance['InstanceType']
        self.state = instance['State']['Name']
        self.state_code = int(instance['State']['Code'])

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('AWS.[A-Z]{1,2}([0-9]{2,3})', self.name)
        if result:
            self.increment = int(result.group(1))
        else:
            self.increment = 0

    def _get_tags(self, client: boto3.client.__class__):
        Tags :list
        try:
            Tags = client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.id]}])['Tags']
        except:
            Tags = []
        return Tags
        
    def print(self):
        super().print()
        print(f"    id                  : {self.id}")
        print(f"    type                : {self.type}")
        print(f"    state               : {self.state} ({self.state_code})")
        