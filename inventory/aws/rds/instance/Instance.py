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
        'Id': 'DBInstanceIdentifier',
        'Name': 'DBInstanceIdentifier',
        'Type': 'DBInstanceClass',
        'State': 'DBInstanceStatus',
        'Arn': 'DBInstanceArn'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: AwsClient):
        self._client = client
        super().__init__(category=f"rds.instance", id=f"{instance['DBInstanceIdentifier']}", object=instance)

        self.SetProperty('AccountId', self.GetProperty('Arn').split(':')[4])
        self.SetProperty('Region', self.GetProperty('Arn').split(':')[3])

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('.{2}aws.{3}([0-9]{3})', self.GetProperty('Name'))
        if result:
            self.SetProperty('Increment', int(result.group(1)))
        else:
            # Nouvelle convetion de nommage
            result = re.match('aws[a-z0-9]{2}rds([0-9]{3})', self.GetProperty('Name'))
            if result:
                self.SetProperty('Increment', int(result.group(1)))
            else:
                self.SetProperty('Increment', 0)

    #
    # Protected methods
    #
    def _get_tags(self):
        try:
            self._tags = self._client.Client().list_tags_for_resource(ResourceName=self.GetProperty('DBInstanceArn'))['TagList']
        except:
            self._tags = []
        return self._tags
