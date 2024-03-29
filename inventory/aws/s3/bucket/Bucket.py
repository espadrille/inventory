# Bucket S3

#
# Imports
#
from datetime import datetime
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

#
# Classe Instance
#
class Bucket(AwsResource):
    _client : AwsClient
    _properties_mapping = {
        'id': 'Name',
        'name': 'Name'
        }

    #
    # Private methods
    #
    def __init__(self, bucket: dict, client: AwsClient):
        self._client = client
        super().__init__(category="s3.bucket", id=f"{bucket['Name']}", object=bucket)

        self.SetProperty('arn', f"arn:aws:s3:::{self.Name()}")
        self.SetProperty('region', client.Client().meta._client_config._user_provided_options['region_name'])

        # Versioning
        if 'Status' in self._client.Client().get_bucket_versioning(Bucket=bucket['Name']):
            self.SetProperty('versioning', self._client.Client().get_bucket_versioning(Bucket=bucket['Name'])['Status'])
        else:
            self.SetProperty('versioning', 'None')

        # Encryption
        self.SetProperty('encryption_type', self._client.Client().get_bucket_encryption(Bucket=bucket['Name'])['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])

    #
    # Protected methods
    #
    def _get_tags(self):
        Tags = []
        try:
            Tags = self._client.Client().get_bucket_tagging(Bucket=self._id)['TagSet']
        except:
            Tags = []
        return Tags
        
