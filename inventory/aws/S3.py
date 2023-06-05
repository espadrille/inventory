# Service S3

#
# Imports
#
import boto3
# from .Aws import Aws
from .AwsService import AwsService
from .s3.bucket.Bucket import Bucket

#
# Classe S3
#
class S3(AwsService):
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, session, client: boto3.client.__class__):
        self._resource_types=['bucket']
        super().__init__(id=f"aws.{session.profile_name}.s3", name='s3', session=session, client=client)
        
    def LoadResources(self) -> dict:

        for my_resource_type in self._resource_types:
            if my_resource_type == "bucket":
                nb_buckets = 0

                for my_bucket in self._client.list_buckets()["Buckets"]:
                    nb_buckets = nb_buckets + 1
                    new_resource = Bucket(bucket=my_bucket, client=self._client) # type: ignore
                    new_resource.SetProperty('profile', self._profile)

                    self._resources[my_resource_type][new_resource.Id()] = new_resource
                    self._resources['all'][new_resource.Id()] = new_resource
                self._summary['buckets'] = str(nb_buckets)

        return self._resources
