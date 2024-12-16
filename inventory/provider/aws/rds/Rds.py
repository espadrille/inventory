'''
    Module de classe Rds
'''

#
# Imports
#
from ..AwsService import AwsService
from .instance.Instance import Instance
from ....core.Console import console

class Rds(AwsService):
    '''
        Classe Rds
    '''
    _db_instance_increments :list # Liste des increments d'instances RDS utilises

    def __init__(self, config :dict=None):
        '''
            Construceur de la classe
        '''
        if config is None:
            config = {}
        config["id"] = "rds"
        config["name"] = "RDS"
        self._is_regional = True
        super().__init__(config=config)
        
        self._db_instance_increments = []

    def LoadResources(self) -> dict:
        '''
            Chargement des ressources
        '''
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

                        if new_resource.GetProperty('Increment') not in  self._db_instance_increments:
                            self._db_instance_increments.append(new_resource.GetProperty('Increment'))
                    self._summary['instances'] = str(nb_instances)
            console.Debug(f" ==> {nb_resources_client} resources.")

        return self._resources

    def NextInstanceIncrement(self):
        '''
            Calcule le prochain increment libre pour une nouvelle instance
        '''
        if len(self._db_instance_increments) > 0:
            for i in range(1, max(self._db_instance_increments)):
                if i not in self._db_instance_increments:
                    return i
        return len(self._db_instance_increments) + 1

    def Print(self):
        '''
            Affiche l'objet
        '''
        self._summary['increment disponible'] = self.NextInstanceIncrement()
        super().Print()
