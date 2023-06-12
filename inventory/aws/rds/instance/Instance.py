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
        'id': 'DBInstanceIdentifier',
        'name': 'DBInstanceIdentifier',
        'type': 'DBInstanceClass',
        'state': 'DBInstanceStatus'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: boto3.client.__class__):
        super().__init__(id=f"rds.instance.{instance['DBInstanceIdentifier']}", object=instance, client=client)

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('.{2}aws.{3}([0-9]{3})', self.GetProperty('name'))
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
            Tags = self._client.list_tags_for_resource(ResourceName=self._properties['arn'])['TagList']
        except:
            Tags = []
        return Tags
