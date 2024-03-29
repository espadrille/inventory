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
        'id': 'DBInstanceIdentifier',
        'name': 'DBInstanceIdentifier',
        'type': 'DBInstanceClass',
        'state': 'DBInstanceStatus',
        'arn': 'DBInstanceArn'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: AwsClient):
        self._client = client
        super().__init__(category=f"rds.instance", id=f"{instance['DBInstanceIdentifier']}", object=instance)

        self.SetProperty('account_id', self.GetProperty('arn').split(':')[4])
        self.SetProperty('region', self.GetProperty('arn').split(':')[3])

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
            Tags = self._client.Client().list_tags_for_resource(ResourceName=self._properties['DBInstanceArn'])['TagList']
        except:
            Tags = []
        return Tags
