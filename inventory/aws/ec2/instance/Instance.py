'''
    Instance EC2
'''

#
# Imports
#
import re
from ...AwsClient import AwsClient
from ...AwsResource import AwsResource

class Instance(AwsResource):
    '''
        Classe Instance
    '''

    _client : AwsClient
    _properties_mapping = {
        'Id': 'InstanceId'
        }

    #
    # Private methods
    #
    def __init__(self, instance: dict, client: AwsClient):
        self._client = client
        self._tags = []
        super().__init__(category="ec2.instance", id=f"{instance['InstanceId']}", object=instance)

        self.SetProperty('AccountId', client.Client().describe_instances()['Reservations'][0]['OwnerId'])
        self.SetProperty('Region', client.Region())
        self.SetProperty('Arn', f"arn:aws:ec2:{self.GetProperty('Region')}:{self.GetProperty('AccountId')}:instance/{self.Id()}")

        if instance['State']['Name'] == 'running':
            self.SetProperty('State', 'poweredOn')
        elif instance['State']['Name'] == 'stopped':
            self.SetProperty('State', 'poweredOff')
        else:
            self.SetProperty('State', instance['State']['Name'])
        self.SetProperty('StateCode', int(instance['State']['Code']))

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('AWS.[A-Z]{1,2}([0-9]{2,3})', self.GetProperty('Name'))
        if result:
            self.SetProperty('Increment', int(result.group(1)))
        else:
            # Nouvelle convetion de nommage
            result = re.match('aws[a-z0-9]{5}([0-9]{3})', self.GetProperty('Name'))
            if result:
                self.SetProperty('Increment', int(result.group(1)))
            else:
                self.SetProperty('Increment', 0)

        # Creation des proprietes NetworkInterface
        i = 0
        for my_interface in self.GetProperty('NetworkInterfaces'):
            i += 1
            self.SetProperty(f"NetworkInterface_{i}", my_interface['NetworkInterfaceId'])
            self.SetProperty(f"PrivateIpAddress_{i}", my_interface['PrivateIpAddress'])
            self.SetProperty(f"SubnetId_{i}", my_interface['SubnetId'])
            subnet = client.Client().describe_subnets(SubnetIds=[my_interface['SubnetId']])['Subnets'][0]
            for my_tag in subnet['Tags']:
                if my_tag['Key'] == 'Name':
                    self.SetProperty(f"SubnetName_{i}", my_tag['Value'])

        # Recherche de la date de creation (= date d'attachement du volume racine)
        for my_device in self.GetProperty('BlockDeviceMappings'):
            if my_device['DeviceName'] == self.GetProperty('RootDeviceName'):
                self.SetProperty('CreationTime', my_device['Ebs']['AttachTime'])


    #
    # Protected methods
    #
    def _get_tags(self):
        try:
            self._tags = self._client.Client().describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('Id')]}])['Tags']
        except Exception:
            self._tags = []
        return self._tags
