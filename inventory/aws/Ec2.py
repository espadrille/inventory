# Service EC2

#
# Imports
#
import boto3
# from .Aws import Aws
from .AwsService import AwsService
from .ec2.instance.Instance import Instance
from .ec2.security_group.SecurityGroup import SecurityGroup

#
# Classe Ec2
#
class Ec2(AwsService):
    _instance_increments :list # Liste des increments d'instances EC2 utilises
    _resource_types : list # Liste des types de ressources a lister pour le service

    def __init__(self, session, client: boto3.client.__class__):
        self._resource_types=['instance', 'security_group']

        super().__init__(id=f"aws.{session.profile_name}.ec2.{client._client_config.region_name}", name='ec2', session=session, client=client)
        self._instance_increments = []
        
    def LoadResources(self) -> dict:
        for my_resource_type in self._resource_types:

            if my_resource_type == 'instance':

                for my_reservation in self._client.describe_instances()['Reservations']:

                    for my_instance in my_reservation['Instances']:
                        new_resource = Instance(instance=my_instance, client=self._client) # type: ignore
                        new_resource.SetProperty('profile', self._profile)

                        self._resources[my_resource_type][new_resource.Id()] = new_resource
                        self._resources['all'][new_resource.Id()] = new_resource
                        if not new_resource.GetProperty('increment') in  self._instance_increments:
                            self._instance_increments.append(new_resource.GetProperty('increment'))

            if my_resource_type == 'security_group':

                for my_sg in self._client.describe_security_groups()['SecurityGroups']: # type: ignore

                    new_resource = SecurityGroup(security_group=my_sg, client=self._client) # type: ignore
                    new_resource.SetProperty('profile', self._profile)

                    self._resources[my_resource_type][new_resource.Id()] = new_resource
                    self._resources['all'][new_resource.Id()] = new_resource

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
