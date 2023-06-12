# Bucket S3

#
# Imports
#
import boto3
from datetime import datetime
from ...AwsResource import AwsResource

#
# Classe Instance
#
class Bucket(AwsResource):
    _properties_mapping = {
        'id': 'Name',
        'name': 'Name'
        }

    #
    # Private methods
    #
    def __init__(self, bucket: dict, client: boto3.client.__class__):
        super().__init__(id=f"s3.bucket.{bucket['Name']}", object=bucket, client=client)

        # Versioning
        if 'Status' in self._client.get_bucket_versioning(Bucket=self.GetProperty('id')):
            self.SetProperty('versioning', self._client.get_bucket_versioning(Bucket=self.GetProperty('id'))['Status'])
        else:
            self.SetProperty('versioning', 'None')

        # Encryption
        self.SetProperty('encryption_type', self._client.get_bucket_encryption(Bucket=self.GetProperty('id'))['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])

    #
    # Protected methods
    #
    def _get_tags(self):
        Tags = []
        try:
            Tags = self._client.get_bucket_tagging(Bucket=self._id)['TagSet']
        except:
            Tags = []
        return Tags
        
