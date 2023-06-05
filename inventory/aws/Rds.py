# Service RDS

#
# Imports
#
import boto3
# from .Aws import Aws
from .AwsService import AwsService
from .rds.instance.Instance import Instance

#
# Classe Rds
#
class Rds(AwsService):
    _db_instance_increments :list # Liste des increments d'instances RDS utilises

    def __init__(self, session, client: boto3.client.__class__):
        self._resource_types=['db_instance']
        
        super().__init__(id=f"aws.{session.profile_name}.rds.{client._client_config.region_name}", name='rds', session=session, client=client)
        self._db_instance_increments = []
        
    def LoadResources(self) -> dict:

        for my_resource_type in self._resource_types:
            if my_resource_type == "db_instance":
                nb_instances = 0

                for my_instance in self._client.describe_db_instances()['DBInstances']:
                    nb_instances = nb_instances + 1

                    new_resource = Instance(instance=my_instance, client=self._client) # type: ignore
                    new_resource.SetProperty('profile', self._profile)

                    self._resources[my_resource_type][new_resource.Id()] = new_resource
                    self._resources['all'][new_resource.Id()] = new_resource
                    if not new_resource.GetProperty('increment') in  self._db_instance_increments:
                        self._db_instance_increments.append(new_resource.GetProperty('increment'))
                self._summary['instances'] = str(nb_instances)

        return self._resources

    def NextInstanceIncrement(self):
        if len(self._db_instance_increments) > 0:
            for i in range(1, max(self._db_instance_increments)):
                if not i in self._db_instance_increments:
                    return i
        return len(self._db_instance_increments) + 1

    def print(self):
        self._summary['increment disponible'] = self.NextInstanceIncrement()
        super().print()
