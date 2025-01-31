'''
    Instance EC2
'''

#
# Imports
#
import re
import json
from .....core.constants import ENVIRONMENT_TYPES
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

        # Distinction Prod/Hors-prod
        self.SetProperty('Environment', client.Profile())
        if self.GetProperty('Environment') in ENVIRONMENT_TYPES:
            self.SetProperty('EnvironmentType', ENVIRONMENT_TYPES[self.GetProperty('Environment')])
        else:
            self.SetProperty('EnvironmentType', 'Unknown')

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
        subnets = ""
        for my_interface in self.GetProperty('NetworkInterfaces'):
            i += 1
            self.SetProperty(f"NetworkInterface_{i}", my_interface['NetworkInterfaceId'])
            self.SetProperty(f"PrivateIpAddress_{i}", my_interface['PrivateIpAddress'])
            self.SetProperty(f"SubnetId_{i}", my_interface['SubnetId'])
            subnet = client.Client().describe_subnets(SubnetIds=[my_interface['SubnetId']])['Subnets'][0]
            for my_tag in subnet['Tags']:
                if my_tag['Key'] == 'Name':
                    self.SetProperty(f"SubnetName_{i}", my_tag['Value'])
                    if subnets == "":
                        subnets = my_tag['Value']
                    else:
                        subnets = f"{subnets}, {my_tag['Value']}"

        # Recherche de la date de creation (= date d'attachement du volume racine)
        for my_device in self.GetProperty('BlockDeviceMappings'):
            if my_device['DeviceName'] == self.GetProperty('RootDeviceName'):
                self.SetProperty('CreationTime', my_device['Ebs']['AttachTime'])

        #
        # Recherche des informations sur l'OS
        # 
        
        self.SetProperty('OsType', 'Windows' if self.GetProperty('PlatformDetails') == 'Windows' else 'Linux')
        self.SetProperty('OsName', self.GetProperty('PlatformDetails'))
        self.SetProperty('OsDetailed', self.GetProperty('PlatformDetails'))

        # Surcharger avec le tag 'os_type' si possible
        try:
            os_type = json.loads(self._get_tag_value("os_type"))
            if os_type:
                self.SetProperty('OsName', os_type['name'])
                self.SetProperty('OsDetailed', os_type['detailed'])
        except json.JSONDecodeError:
            pass

        # Surcharger avec le tag 'cartography' si possible
        try:
            cartography = json.loads(self._get_tag_value('cartography'))
            if cartography:
                if 'os' in cartography:
                    if 'type' in cartography['os']:
                        self.SetProperty('OsType', cartography['os']['type'])
                    if 'name' in cartography['os']:
                        self.SetProperty('OsName', cartography['os']['name'])
                    if 'detailed' in cartography['os']:
                        self.SetProperty('OsDetailed', cartography['os']['detailed'])
        except json.JSONDecodeError:
            pass


    #
    # Protected methods
    #
    def _get_tags(self):
        try:
            self._tags = self._client.Client().describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.GetProperty('Id')]}])['Tags']
        except Exception:
            self._tags = []
        return self._tags
