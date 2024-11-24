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

from ...Console import console
from ...ConfigurableObject import ConfigurableObject
from .virtualmachine.VirtualMachine import VirtualMachine

class Datacenter(ConfigurableObject):
    '''
        Classe Datacenter
    '''

    _service_instance :vim.ServiceInstance
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

        # Informations de connexion
        self.SetProperty('hostname', self._get_config_value(config['hostname']))
        self.SetProperty('user', self._get_config_value(config['user']))
        self.SetProperty('password', self._get_config_value(config['password']))

        console.Debug(text=f"Datacenter hostname={self.GetProperty('hostname')}")
        console.Debug(text=f"Datacenter user={self.GetProperty('user')}")

        console.Debug(text=f"config['folders']={config['folders']}")

        context = ssl._create_unverified_context()

        # Connexion au serveur vCenter
        try:
            self._service_instance = SmartConnect(host=self.GetProperty('hostname'),
                                            user=self.GetProperty('user'),
                                            pwd=self.GetProperty('password'),
                                            sslContext=context)

            self._content = self._service_instance.RetrieveContent()

            # S'assurer que la déconnexion se fera a la fin du programme
            atexit.register(Disconnect, self._service_instance)
        except Exception:
            console.Print(text=f"Erreur lors de la connexion a VSphere ({self.GetProperty('hostname')})", text_format="ERROR")

        # Connexion au serveur vCenter
        try:
            self._content = self._service_instance.RetrieveContent()
        except Exception:
            console.Print(text=f"Erreur lors de la lecture du contenu de VSphere ({self.GetProperty('hostname')})", text_format="ERROR")

    #
    # Public methods
    #
    def Id(self):
        '''
            Retourne l'identifant de l'objet
        '''
        return self.GetProperty('id')

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
