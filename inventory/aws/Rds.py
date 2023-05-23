# Service RDS

#
# Imports
#
import boto3
# from .Aws import Aws
from .Service import Service
from .rds.instance.Instance import Instance

#
# Classe Rds
#
class Rds(Service):
    _db_instance_increments :list # Liste des increments d'instances RDS utilises

    def __init__(self, id: str, name: str=""):
        self._resource_types=['db_instance']
        
        super().__init__(id=id, name=name)
        self._db_instance_increments = []
        
    def LoadResources(self, profile_name: str="") -> dict:
        if profile_name != "":
            self.SetProfile(profile_name=profile_name)
        print(f"   ==> Service {self.name} sur Environnement {self._profile} <==")
        self._client = boto3.Session(profile_name=self._profile).client(service_name="rds") # type: ignore
        for my_resource_type in self._resource_types:
            if my_resource_type == "db_instance":
                for my_instance in self._client.describe_db_instances()['DBInstances']:
                    new_resource = Instance(instance=my_instance, client=self._client) # type: ignore
                    new_resource.profile = self._profile

                    self._resources[my_resource_type][new_resource.id] = new_resource
                    self._resources['all'][new_resource.id] = new_resource
                    if not new_resource.increment in  self._db_instance_increments:
                        self._db_instance_increments.append(new_resource.increment)
        return self._resources

    def NextInstanceIncrement(self):
        if len(self._db_instance_increments) > 0:
            for i in range(0, max(self._db_instance_increments)):
                if not i in self._db_instance_increments:
                    return i
        return len(self._db_instance_increments) + 1

    def print(self):
        super().print()
        print(f"increment d'instance disponible : {self.NextInstanceIncrement()}")
