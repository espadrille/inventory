# VSphere Machine virtuelle

#
# Imports
#
import re
import requests
from ....Console import console
from ...VsphereResource import VsphereResource

#
# Classe Instance
#
class VirtualMachine(VsphereResource):
    _datacenter=None
    _properties_mapping = {
        }

    #
    # Private methods
    #
    def __init__(self, vm: dict, datacenter=None):
        self._datacenter = datacenter
        super().__init__(category=f"virtual_machine", id=f"{vm.vm._moId}", resource=vm)

        self.SetProperty('Name', vm.config.name)
        self.SetProperty('Hypervisor', vm.runtime.host._stub.pool[0][0].sock.server_hostname)
        self.SetProperty('HostVersion', re.match('.*\/([0-9\.]*).*', vm.runtime.host._stub.versionId).group(1))
        host = vm.runtime.host
        self.SetProperty('Host', host.name)
        self.SetProperty('fqdn', vm.guest.hostName)
        self.SetProperty('PrivateIpAddress', vm.guest.ipAddress)
        self.SetProperty('State', vm.runtime.powerState)
        self.SetProperty('guestFullName', vm.config.guestFullName) 
        self.SetProperty('bootTime', vm.runtime.bootTime)
        self.SetProperty('annotation', vm.config.annotation)

        # Tenter de lire l'increment dans le nom de l'instance
        result = re.match('[A-Z]{5,6}([0-9]{2,3})', self.GetProperty('Name'))
        if result:
            self.SetProperty('Increment', int(result.group(1)))
        else:
            # Nouvelle convetion de nommage
            result = re.match('[a-z0-9]{8}([0-9]{3})', self.GetProperty('Name'))
            if result:
                self.SetProperty('Increment', int(result.group(1)))
            else:
                self.SetProperty('Increment', 0)

        # Recherche de la date de creation (= date d'attachement du volume racine)
        for my_device in self.GetProperty('BlockDeviceMappings'):
            if my_device['DeviceName'] == self.GetProperty('RootDeviceName'):
                self.SetProperty('CreationTime', my_device['Ebs']['AttachTime'])

        # Ajouter des proprietes basees sur le contenu des tags
        if len(self._get_tags()) > 0:
            if self._get_tag_value('Veeam') != "":
                self.SetProperty('BALISES_VEEAM', self._get_tag_value('Veeam'))
            if self._get_tag_value('BALISES_NETBACKUP') != "":
                self.SetProperty('BALISES_NETBACKUP', self._get_tag_value('BALISES_NETBACKUP'))
            if self._get_tag_value('ENVIRONNEMENT') != "":
                self.SetProperty('BALISES_Environnement', self._get_tag_value('ENVIRONNEMENT'))
            if self._get_tag_value('Guest OS') != "":
                self.SetProperty('BALISES_GuestOS', self._get_tag_value('Guest OS'))

    #
    # Protected methods
    #
    def _get_tags(self):
        try:
            # La recherche des tags se fait par call d'API car pyvmomi ne prend pas en cherge le recuperation des tags
            #

            session = requests.Session()

            # Desctiver les avertissements lies au certificat
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

            base_url = f"https://{self._datacenter.GetProperty('hostname')}"

            # Authentification
            response = session.post(f"{base_url}/rest/com/vmware/cis/session", auth=(self._datacenter.GetProperty('user'), self._datacenter.GetProperty('password')), verify=False)
            if response.status_code != 200:
                raise Exception("Echec de l'authentification a vSphere")
            session_id = response.json()['value']
            headers = {
                'vmware-api-session-id': session_id,
                'Content-Type': 'application/json'
            }

            # Recupération des tags associes à la machine virtuelle
            request_url = f"{base_url}/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-tags"
            payload = {
                "object_id": {
                    "id": self.GetProperty('id'),
                    "type": "VirtualMachine"
                }
            }
            response = requests.post(request_url, headers=headers, json=payload, verify=False)
            if response.status_code != 200:
                raise Exception(f"Erreur {response.status_code} lors de la lecture des tags associes a la machine virtuelle {self.GetProperty('Name')}.\nurl={request_url}\nPayload={payload}")
            tag_ids = response.json()['value']

            # Recuperation des details des tags
            self._tags = []
            for tag_id in tag_ids:
                tag_detail_url = f"{base_url}/rest/com/vmware/cis/tagging/tag/id:{tag_id}"
                tag_detail_response = requests.get(tag_detail_url, headers=headers, verify=False)
                if tag_detail_response.status_code != 200:
                    raise Exception(f"Erreur {response.status_code} lors de la lecture des details du tag {tag_id}.\nurl={tag_detail_url}")
                else:
                    tag_info = tag_detail_response.json()['value']
                    tag_name = tag_info['name']
                    category_id = tag_info['category_id']
                    category_detail_url = f"{base_url}/rest/com/vmware/cis/tagging/category/id:{category_id}"
                    category_detail_response = requests.get(category_detail_url, headers=headers, verify=False)
                    if category_detail_response.status_code != 200:
                        raise Exception(f"Erreur {response.status_code} lors de la lecture des details de la categorie {category_id}.\nurl={category_detail_url}")
                    else:
                        category_info = category_detail_response.json()['value']
                        category_name = category_info['name']
                        self._tags.append({
                            "Key": category_name,
                            "Value":tag_name
                            })

        except Exception as e:
            console.Print(f"Erreur de recuperation des tags : {e}")
            self._tags = []
        return self._tags
        
