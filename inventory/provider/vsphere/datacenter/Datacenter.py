'''
    Module Datacenter
'''

#
# Imports
#
import ssl
import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import urllib3
import requests

from ....core.Console import console
from ....core.ConfigurableObject import ConfigurableObject
from .virtualmachine.VirtualMachine import VirtualMachine

class Datacenter(ConfigurableObject):
    '''
        Classe Datacenter
    '''

    _service_instance :vim.ServiceInstance
    _API_session: requests.Session
    _API_session_id: str

    _is_vmomi_connected: bool
    _is_api_connected: bool

    _content :vim.ServiceInstanceContent
    _resources :dict
    _folders :dict
    _vm_increments :list # Liste des increments des machines virutelles utilises
    _summary: dict

    #
    # Private methods
    #
    def __init__(self, name:str, config :dict=None):
        '''
            Initialisation de l'objet
        '''
        if config is None:
            config = {}

        super().__init__(config=config)
        self.SetProperty('id', name)
        self.SetProperty('name', name)
        if self.GetProperty('name') == '':
            self.SetProperty('name', self.GetProperty('id'))
        self._resources = {}
        self._resources['all'] = {}
        self._vm_increments = []
        self._summary = {}
        self._is_vmomi_connected = False
        self._is_api_connected = False

        # Informations de connexion
        self.SetProperty('hostname', self._get_config_value(config['hostname']))
        self.SetProperty('user', self._get_config_value(config['user']))
        self.SetProperty('password', self._get_config_value(config['password']))

        console.Debug(text=f"Datacenter hostname={self.GetProperty('hostname')}")
        console.Debug(text=f"Datacenter user={self.GetProperty('user')}")

        console.Debug(text=f"config['folders']={config['folders']}")

    #
    # Protected methods
    #
    def _connect_api(self):
        # Ouverture d'une session API
        try:
            self._API_session = requests.Session()

            # Desctiver les avertissements lies au certificat
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            base_url = f"https://{self.GetProperty('hostname')}"

            # Authentification
            request_url = f"{base_url}/rest/com/vmware/cis/session"
            response = self._API_session.post(request_url, auth=(self.GetProperty('user'), self.GetProperty('password')), verify=False, timeout=60)
            if response.status_code != 200:
                raise requests.HTTPError(
                    "Echec de l'authentification a vSphere\n"
                    f"url={request_url}\n"
                    f"user={self.GetProperty('user')}"
                    )
            # print(self._API_session.cookies)
            self._API_session_id = self._API_session.cookies.get('vmware-api-session-id', domain=self.GetProperty('hostname'), path="/rest")
            console.Print(text=f"Session API ouverte sur {self.GetProperty('hostname')} (session_id={self._API_session_id})", text_format="GREEN")
            self._is_api_connected = True
            # S'assurer que la déconnexion se fera a la fin du programme
            atexit.register(self._disconnect_api, self._service_instance)
        except Exception as e:
            console.Print(text=f"Erreur lors de la connexion a VSphere API ({self.GetProperty('hostname')})", text_format="ERROR")
            console.Print(text=f"Exception ({e})", text_format="ERROR")

    def _connect_vmomi(self):
        # Connexion au serveur vCenter
        context = ssl._create_unverified_context()
        try:
            self._service_instance = SmartConnect(host=self.GetProperty('hostname'),
                                            user=self.GetProperty('user'),
                                            pwd=self.GetProperty('password'),
                                            sslContext=context)
            self._is_vmomi_connected = True
            # S'assurer que la déconnexion se fera a la fin du programme
            atexit.register(Disconnect, self._service_instance)
        except Exception as e:
            console.Print(text=f"Erreur lors de la connexion a VSphere vmomi ({self.GetProperty('hostname')})", text_format="ERROR")
            console.Print(text=f"Exception ({e})", text_format="ERROR")

        # Lecture du contenu du vCenter
        try:
            self._content = self._service_instance.RetrieveContent()
        except Exception:
            console.Print(text=f"Erreur lors de la lecture du contenu de VSphere ({self.GetProperty('hostname')})", text_format="ERROR")

    def _disconnect_api(self, *args, **kwargs):
        # Fermer la session API si on n'en a plus besoin
        try:
            response = self._API_session.delete(f"https://{self.GetProperty('hostname')}/rest/com/vmware/cis/session", verify=False)
            if response.status_code == 200:
                console.Print(text=f"Session API terminee sur ({self.GetProperty('hostname')}) (session_id={self._API_session_id})", text_format="GREEN")
                self._is_api_connected = False
        except requests.exceptions.SSLError as e:
            console.Print(text=f"Erreur lors de la fermeture de la session API sur ({self.GetProperty('hostname')}) (session_id={self._API_session_id})", text_format="ERROR")

    #
    # Public methods
    #
    def APISession(self):
        '''
            Retourne la session d'API ouverte
        '''
        return self._API_session

    def APISessionId(self):
        '''
            Retourne l'id de la session d'API ouverte
        '''
        return self._API_session_id

    def CallRestAPI(self, path: str="/", method: str="GET", payload: dict={}):
        if self._is_api_connected:
            try:
                request_url = f"https://{self.GetProperty('hostname')}{path}"
                headers = {
                    'vmware-api-session-id': self._API_session_id,
                    'Content-Type': 'application/json'
                }
                if method =='POST':
                    response = self._API_session.post(request_url, headers=headers, json=payload, verify=False, timeout=60)
                elif method =='GET':
                    response = self._API_session.get(request_url, headers=headers, verify=False, timeout=60)

                if response.status_code != 200:
                    raise requests.HTTPError(
                        f"Code rtour API HTTP/{response.status_code} lors de l'apelle d'API {request_url} [{method}].\n"
                        f"Payload={payload}"
                        )
            except Exception as e:
                console.Print(text=f"Erreur lors de l'appel d'API ({request_url}) [{method}]", text_format="ERROR")
                console.Print(text=f"Exception: ({e})", text_format="ERROR")
        else:
            console.Print(text=f"Aucune session API ouverte sur ({self.GetProperty('hostname')})", text_format="ERROR")
        return response

    def Connect(self):
        self._connect_vmomi()
        self._connect_api()
        return self.IsConnected()

    def Id(self):
        '''
            Retourne l'identifant de l'objet
        '''
        return self.GetProperty('id')

    def IsConnected(self) -> bool:
        '''
            Indique si le datacenter est connecte
        '''
        return self._is_vmomi_connected and self._is_api_connected

    def Name(self):
        '''
            Retourne le nom de l'objet
        '''
        return self.GetProperty('name')

    def LoadResources(self) -> dict:
        '''
            Charge les ressources du datacenter
        '''
        nb_vms = 0
        self._resources['all'] = {}

        if not self.IsConnected():
            return {}

        for my_folder in self._config['folders']:
            nb_resources_folder = 0
            console.Debug(f"  Chargement : {my_folder}")

            for my_resource_type in self._config['folders'][my_folder]['resource_types']:
                self._resources[my_resource_type] = {}

                if my_resource_type == 'virtual_machine':

                    # Lister les machines virtuelles
                    obj_view = self._content.viewManager.CreateContainerView(self._content.rootFolder, [vim.VirtualMachine], True)
                    vms = obj_view.view
                    obj_view.Destroy()

                    for my_vm in vms:
                        nb_vms = nb_vms + 1

                        new_resource = VirtualMachine(vm=my_vm, datacenter=self)

                        console.Debug(f"    {my_folder} charge : {new_resource.GetProperty('Name')} ")

                        self._resources[my_resource_type][new_resource.Id()] = new_resource
                        self._resources['all'][new_resource.Id()] = new_resource
                        nb_resources_folder += 1

                        if new_resource.GetProperty('Increment') not in  self._vm_increments:
                            self._vm_increments.append(new_resource.GetProperty('Increment'))

                        # Pour limiter le nombre de machines virutelles extraites
                        # if nb_vms > 9 : break

                    self._summary[my_resource_type] = str(nb_vms)

            console.Debug(f"  Folder {my_folder} ==> {nb_resources_folder} resources.")

        self._summary['resources total'] = str(len(self._resources['all']))

        return self._resources
