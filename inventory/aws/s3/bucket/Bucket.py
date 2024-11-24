'''
    Module de classe Bucket
'''

#
# Imports
#
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

class Bucket(AwsResource):
    '''
        Classe Bucket
    '''

    _client : AwsClient
    _properties_mapping = {
        'Id': 'id',
        'Name': 'id'
        }

    #
    # Private methods
    #
    def __init__(self, bucket: dict, client: AwsClient):
        '''
            Constructeur de la classe
        '''

        self._client = client
        super().__init__(category="s3.bucket", id=f"{bucket['Name']}", object=bucket)

        self.SetProperty('Arn', f"arn:aws:s3:::{self.GetProperty('Name')}")
        self.SetProperty('Region', client.Client().meta._client_config._user_provided_options['region_name'])

        # Versioning
        if 'Status' in self._client.Client().get_bucket_versioning(Bucket=bucket['Name']):
            self.SetProperty('Versioning', self._client.Client().get_bucket_versioning(Bucket=bucket['Name'])['Status'])
        else:
            self.SetProperty('Versioning', 'None')

        # Encryption
        self.SetProperty('EncryptionType', self._client.Client().get_bucket_encryption(Bucket=bucket['Name'])['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])

    #
    # Protected methods
    #
    def _get_tags(self):
        '''
            Retourne les tags
        '''

        try:
            self._tags = self._client.Client().get_bucket_tagging(Bucket=self.GetProperty('id'))['TagSet']
        except Exception:
            self._init_tags()
        return self._tags
