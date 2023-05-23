# Service S3

#
# Imports
#
import boto3
# from .Aws import Aws
from .Service import Service
from .s3.bucket.Bucket import Bucket

#
# Classe S3
#
class S3(Service):
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, id: str, name: str=""):
        self._resource_types=['bucket']

        super().__init__(id=id, name=name)
        
    def LoadResources(self, profile_name: str="") -> dict:
        if profile_name != "":
            self.SetProfile(profile_name=profile_name)
        print(f"   ==> Service {self.name} sur Environnement {self._profile} <==")
        self._client = boto3.Session(profile_name=self._profile).client(service_name="s3") # type: ignore
        for my_resource_type in self._resource_types:
            if my_resource_type == "bucket":
                for my_bucket in self._client.list_buckets()["Buckets"]:
                    new_resource = Bucket(bucket=my_bucket, client=self._client) # type: ignore
                    new_resource.profile = self._profile

                    self._resources[my_resource_type][new_resource.id] = new_resource
                    self._resources['all'][new_resource.id] = new_resource
        return self._resources
