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
    creation_date :datetime
    versioning :str
    encryption_type :str

    def __init__(self, bucket: dict, client: boto3.client.__class__):
        super().__init__(id=bucket['Name'], name=bucket['Name'], client=client)
        self.creation_date = bucket["CreationDate"]

        # Versioning
        if 'Status' in self._client.get_bucket_versioning(Bucket=self.id):
            self.versioning = self._client.get_bucket_versioning(Bucket=self.id)['Status']
        else:
            self.versioning = 'None'

        # Encryption
        self.encryption_type = self._client.get_bucket_encryption(Bucket=self.id)['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

    def _get_tags(self, client: boto3.client.__class__):
        Tags = []
        try:
            Tags = client.get_bucket_tagging(Bucket=self.id)['TagSet']
        except:
            Tags = []
        return Tags
        

    def print(self):
        super().print()
        print(f"    date creation       : {self.creation_date.strftime('%d/%m/%Y %H:%m:%S')}")
        print(f"    versionning         : {self.versioning}")
        print(f"    encryption_type     : {self.encryption_type}")
        