# Service RDS

#
# Imports
#
# from .Aws import Aws
from ..AwsService import AwsService
from .instance.Instance import Instance
from ...Console import console

#
# Classe Rds
#
class Rds(AwsService):
    _db_instance_increments :list # Liste des increments d'instances RDS utilises

    def __init__(self, config :dict={}):
        config["id"] = "rds"
        config["name"] = "RDS"
        self._is_regional = True
        super().__init__(config=config)
        
        self._db_instance_increments = []
        
    def LoadResources(self) -> dict:
        nb_instances = 0
        self._resources['all'] = {}
        for my_client in self._clients:
            nb_resources_client = 0
            console.Debug(f"  Chargement : {my_client.Name()}", newline=False)

            for my_resource_type in self._config["resource_types"]:
                if my_resource_type == "db_instance":
                    nb_instances = 0

                    for my_instance in my_client.Client().describe_db_instances()['DBInstances']:
                        nb_instances = nb_instances + 1

                        new_resource = Instance(instance=my_instance, client=my_client) # type: ignore
                        new_resource.SetProperty('Profile', my_client.Profile())

                        self._resources[my_resource_type][new_resource.Id()] = new_resource
                        self._resources['all'][new_resource.Id()] = new_resource
                        nb_resources_client += 1

                        if not new_resource.GetProperty('Increment') in  self._db_instance_increments:
                            self._db_instance_increments.append(new_resource.GetProperty('Increment'))
                    self._summary['instances'] = str(nb_instances)
            console.Debug(f" ==> {nb_resources_client} resources.")

        return self._resources

    def NextInstanceIncrement(self):
        if len(self._db_instance_increments) > 0:
            for i in range(1, max(self._db_instance_increments)):
                if not i in self._db_instance_increments:
                    return i
        return len(self._db_instance_increments) + 1

    def Print(self):
        self._summary['increment disponible'] = self.NextInstanceIncrement()
        super().Print()
