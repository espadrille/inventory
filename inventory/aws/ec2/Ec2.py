# Service EC2

#
# Imports
#
from ..AwsService import AwsService
from .instance.Instance import Instance
from .security_group.SecurityGroup import SecurityGroup
from ...Console import console

#
# Classe Ec2
#
class Ec2(AwsService):
    _instance_increments :list # Liste des increments d'instances EC2 utilises

    def __init__(self, config :dict={}):
        config["id"] = "ec2"
        config["name"] = "Ec2"
        self._is_regional = True
        super().__init__(config=config)
        
        self._instance_increments = []
        
    def LoadResources(self) -> dict:
        nb_instances = 0
        nb_sg = 0
        self._resources['all'] = {}
        for my_client in self._clients:
            nb_resources_client = 0
            console.Debug(f"  Chargement : {my_client.Name()}", newline=False)

            for my_resource_type in self._config["resource_types"]:

                if my_resource_type == 'instance':

                    for my_reservation in my_client.Client().describe_instances()['Reservations']:

                        for my_instance in my_reservation['Instances']:
                            nb_instances = nb_instances + 1

                            new_resource = Instance(instance=my_instance, client=my_client) # type: ignore
                            new_resource.SetProperty('Profile', my_client.Profile())

                            self._resources[my_resource_type][new_resource.Id()] = new_resource
                            self._resources['all'][new_resource.Id()] = new_resource
                            nb_resources_client += 1

                            if not new_resource.GetProperty('Increment') in  self._instance_increments:
                                self._instance_increments.append(new_resource.GetProperty('Increment'))
                    self._summary['instances'] = str(nb_instances)

                if my_resource_type == 'security_group':

                    for my_sg in my_client.Client().describe_security_groups()['SecurityGroups']: # type: ignore
                        nb_sg = nb_sg + 1
                        
                        new_resource = SecurityGroup(security_group=my_sg, client=my_client) # type: ignore
                        new_resource.SetProperty('Profile', my_client.Profile())

                        self._resources[my_resource_type][new_resource.Id()] = new_resource
                        self._resources['all'][new_resource.Id()] = new_resource
                        nb_resources_client += 1

                    self._summary['security-groups'] = str(nb_sg)
            console.Debug(f" ==> {nb_resources_client} resources.")

        self._summary['resources total'] = str(len(self._resources['all']))

        return self._resources

    def NextInstanceIncrement(self):
        if len(self._instance_increments) > 0:
            for i in range(1, max(self._instance_increments)):
                if not i in self._instance_increments:
                    return i
        return max(self._instance_increments) + 1

    def Print(self):
        self._summary['increment disponible'] = self.NextInstanceIncrement()
        super().Print()
