'''
    Module de classe VirutalMachine
'''

#
# Imports
#
import re
from pyVmomi import vim
from ...VsphereResource import VsphereResource

#
# Classe Instance
#
class VirtualMachine(VsphereResource):
    '''
        Classe VirtualMachine
    '''

    _datacenter = None
    _properties_mapping = {
        }
    _vm: vim.VirtualMachine

    #
    # Private methods
    #
    def __init__(self, vm: vim.VirtualMachine, datacenter=None):
        self._vm = vm
        self._datacenter = datacenter
        super().__init__(category="virtual_machine", id=f"{self._vm.summary.vm._moId}", resource=self._vm.summary)

        self.SetProperty('Name', self._vm.summary.config.name)
        self.SetProperty('Datacenter', datacenter.GetProperty('name'))
        self.SetProperty('Hypervisor', self._vm.summary.runtime.host._stub.pool[0][0].sock.server_hostname)
        self.SetProperty('HostVersion', re.match('.*\/([0-9\.]*).*', self._vm.summary.runtime.host._stub.versionId).group(1))
        host = self._vm.summary.runtime.host
        self.SetProperty('Host', host.name)
        self.SetProperty('fqdn', self._vm.summary.guest.hostName)
        self.SetProperty('PrivateIpAddress', self._vm.summary.guest.ipAddress)
        self.SetProperty('State', self._vm.summary.runtime.powerState)
        self.SetProperty('guestFullName', self._vm.summary.config.guestFullName)
        self.SetProperty('bootTime', self._vm.summary.runtime.bootTime)
        self.SetProperty('annotation', self._vm.summary.config.annotation)

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('[A-Z]{5,6}([0-9]{2,3})', self.GetProperty('Name'))
        if result:
            self.SetProperty('Increment', int(result.group(1)))
        else:
            # Nouvelle convention de nommage
            result = re.match('[a-z0-9]{8}([0-9]{3})', self.GetProperty('Name'))
            if result:
                self.SetProperty('Increment', int(result.group(1)))
            else:
                self.SetProperty('Increment', 0)

        # Recherche de la date de creation (= date d'attachement du volume racine)
        # for my_device in self.GetProperty('BlockDeviceMappings'):
        #     if my_device['DeviceName'] == self.GetProperty('RootDeviceName'):
        #         self.SetProperty('CreationTime', my_device['Ebs']['AttachTime'])

        # Ajouter les informations de tags
        self._execute_with_retry(self._get_tags)

        # Ajouter des proprietes basees sur le contenu des tags
        if len(self._tags) > 0:
            if self._get_tag_value('Veeam') != "":
                self.SetProperty('BALISES_VEEAM', self._get_tag_value('Veeam'))
            if self._get_tag_value('BALISES_NETBACKUP') != "":
                self.SetProperty('BALISES_NETBACKUP', self._get_tag_value('BALISES_NETBACKUP'))
            if self._get_tag_value('ENVIRONNEMENT') != "":
                self.SetProperty('BALISES_Environnement', self._get_tag_value('ENVIRONNEMENT'))
            if self._get_tag_value('Guest OS') != "":
                self.SetProperty('BALISES_GuestOS', self._get_tag_value('Guest OS'))

        # Ajouter les informations de reseau
        self._execute_with_retry(self._get_networks)

    #
    # Protected methods
    #
    def _get_tags(self):
        #
        # La recherche des tags se fait par call d'API car pyvmomi ne prend pas en cherge le recuperation des tags
        #
        response = self._datacenter.CallRestAPI(
            path='/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-tags',
            method='POST',
            payload = {
                "object_id": {
                    "id": self.GetProperty('id'),
                    "type": "VirtualMachine"
                    }
                }
            )
        tag_ids = response.json()['value']

        # Recuperation des details des tags
        self._tags = []
        for tag_id in tag_ids:
            response = self._datacenter.CallRestAPI(
                path=f"/rest/com/vmware/cis/tagging/tag/id:{tag_id}",
                method='GET'
                )
            tag_info = response.json()['value']

            response = self._datacenter.CallRestAPI(
                path=f"/rest/com/vmware/cis/tagging/category/id:{tag_info['category_id']}",
                method='GET'
                )
            category_info = response.json()['value']

            self._tags.append({
                "Key": category_info['name'],
                "Value":tag_info['name']
                })

    def _get_networks(self):
        # lire les informations de reseau
        i = 1
        for device in self._vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                self.SetProperty(f'SubnetName_{i}', device.deviceInfo.summary)
