# Service EC2

#
# Imports
#
import boto3
# from .Aws import Aws
from .Service import Service
from .ec2.instance.Instance import Instance
from .ec2.security_group.SecurityGroup import SecurityGroup

#
# Classe Ec2
#
class Ec2(Service):
    _instance_increments :list # Liste des increments d'instances EC2 utilises
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, id: str, name: str=""):
        self._resource_types=['instance', 'security_group']

        super().__init__(id=id, name=name)
        self._instance_increments = []
        
    def LoadResources(self, profile_name: str="") -> dict:
        if profile_name != "":
            self.SetProfile(profile_name=profile_name)
        print(f"   ==> Service EC2 sur Environnement {self._profile} <==")
        self._client = boto3.Session(profile_name=self._profile).client(service_name="ec2") # type: ignore
        for my_resource_type in self._resource_types:
            if my_resource_type == 'instance':
                for my_reservation in self._client.describe_instances()['Reservations']:
                    for my_instance in my_reservation['Instances']:
                        new_resource = Instance(instance=my_instance, client=self._client) # type: ignore
                        new_resource.profile = self._profile

                        self._resources[my_resource_type][new_resource.id] = new_resource
                        self._resources['all'][new_resource.id] = new_resource
                        if not new_resource.increment in  self._instance_increments:
                            self._instance_increments.append(new_resource.increment)
            if my_resource_type == 'security_group':
                for my_sg in self._client.describe_security_groups()['SecurityGroups']: # type: ignore
                    new_resource = SecurityGroup(security_group=my_sg, client=self._client) # type: ignore
                    new_resource.profile = self._profile

                    self._resources[my_resource_type][new_resource.id] = new_resource
                    self._resources['all'][new_resource.id] = new_resource

        return self._resources

    def NextInstanceIncrement(self):
        if len(self._instance_increments) > 0:
            for i in range(0, max(self._instance_increments)):
                if not i in self._instance_increments:
                    return i
        return len(self._instance_increments) + 1

    def print(self):
        super().print()
        print(f"increment d'instance disponible : {self.NextInstanceIncrement()}")
