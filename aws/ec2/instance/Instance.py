# Instance EC2

#
# Imports
#

#
# Classe Instance
#
class Instance:
    name = ""
    instance_id = ""
    client = None

    def __init__(self, client=None, instance_id=""):
        if client is None:
            print("Fournissez un client pour Ec2.Instance")
        else:
            self.client = client
        
        if instance_id != "":
            name = instance_id
            self.LoadInstance(instance_id)

    def LoadInstance(self, instance_id):
        instance = self.client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]

        # Recuperation du tag "Name"
        if 'Tags' in instance:
            t_name = [tag['Value'] for tag in instance['Tags'] if(tag['Key'] == 'Name')]
            if len(t_name) > 0:
                self.name = t_name[0]

    def print(self):
        print(self.name)