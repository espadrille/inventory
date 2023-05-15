# Service EC2

#
# Imports
#

#
# Classe Ec2
#
class Ec2:
    name = "ec2"
    regions = ['eu-west-1', 'eu-west-3']

    clients = {} # Liste des clients (un par region)
    resources = {}

    def __init__(self, session=None, name=""):
        if session is None:
            print("Fournissez une session AWS pour EC2 !")
        else:
            for region in self.regions:
                self.clients[region] = session.client('ec2', region_name=region)

        if name != "":
            self.name = name

        self.LoadResources(resource_type='instance')
        
    def LoadResources(self, resource_type="instance"):
        if resource_type == "instance":
            from .instance.Instance import Instance
            for region in self.regions:
                for reservation in self.clients[region].describe_instances()['Reservations']:
                    for instance in reservation['Instances']:
                        # print(instance['InstanceId'])
                        self.resources[instance['InstanceId']] = Instance(client=self.clients[region], instance_id=instance['InstanceId'])

    def ListResources(self):
        for k_resource, resource in self.resources.items():
            resource.print()

    def print(self):
        print(f"Service : {self.name}")
        for k_resource, resource in self.resources.items():
            resource.print()