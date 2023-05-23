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
    increment :int

    def __init__(self, instance: dict, client: boto3.client.__class__):
        super().__init__(id=instance['DBInstanceIdentifier'], name=instance['DBInstanceIdentifier'], client=client, arn=instance['DBInstanceArn'])
        self.type = instance['DBInstanceClass']
        self.state = instance['DBInstanceStatus']

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('.{2}aws.{3}([0-9]{3})', self.name)
        if result:
            self.increment = int(result.group(1))
        else:
            self.increment = 0

    def _get_tags(self, client: boto3.client.__class__):
        Tags :list
        try:
            Tags = client.list_tags_for_resource(ResourceName=self.arn)['TagList']
        except:
            Tags = []
        return Tags
        
    def print(self):
        super().print()
        print(f"    id                  : {self.id}")
        print(f"    type                : {self.type}")
        print(f"    state               : {self.state}")
        print(f"    increment           : {self.increment}")
        