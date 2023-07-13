# Service S3

#
# Imports
#
from .AwsService import AwsService
from .s3.bucket.Bucket import Bucket
from ..Console import console

#
# Classe S3
#
class S3(AwsService):
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, config :dict={}):
        config["id"] = "s3"
        config["name"] = "S3"
        config["resource_types"] = ["bucket"]
        if "filters" in config:
            if "resource_types" in config["filters"]:
                config["resource_types"] = config["filters"]["resource_types"]
        self._is_regional = False
        super().__init__(config=config)
        
    def LoadResources(self) -> dict:

        for my_client in self._clients:
            nb_resources_client = 0
            console.Debug(f"  Chargement : {my_client.Name()}")
            for my_resource_type in self._config["resource_types"]:
                if my_resource_type == "bucket":
                    nb_buckets = 0

                    for my_bucket in my_client.Client().list_buckets()["Buckets"]:
                        nb_buckets = nb_buckets + 1
                        new_resource = Bucket(bucket=my_bucket, client=my_client) # type: ignore
                        new_resource.SetProperty('profile', my_client.Profile())

                        self._resources[my_resource_type][new_resource.Id()] = new_resource
                        self._resources['all'][new_resource.Id()] = new_resource
                        nb_resources_client += 1

                    self._summary['buckets'] = str(nb_buckets)
            console.Debug(f"  Total client {my_client.Name()} : {nb_resources_client} resources.")

        return self._resources
