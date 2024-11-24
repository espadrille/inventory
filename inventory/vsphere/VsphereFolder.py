'''
    Module de classe VsphereFolder
'''
from ..Console import console
from ..Object import Object

class VsphereFolder(Object):
    '''
        Classe VsphereFolder
    '''

    _client: SmartConnect.__class__

    #
    # Private methods
    #
    def __init__(self, folder: str, config:dict):
        '''
            Constructeur de la classe
        '''
        super().__init__()

        self.SetProperty('Name', )

        console.Debug(f"Creation client : {self.Name()}")

    #
    # Public methods
    #
    def Client(self):
        '''
            Retourne le client
        '''
        return self._client
    
    def Name(self):
        '''
            Retourne le nom du folder
        '''
        return f"{self.GetProperty('service')}.{self.GetProperty('profile')}.{self.GetProperty('region')}"
    
    def Profile(self):
        '''
            Retourne le profile
        '''
        return self.GetProperty('profile')

    def Region(self):
        '''
            Retourne la region
        '''
        return self.GetProperty('region')

    def Service(self):
        '''
            Retourne le service
        '''
        return self.GetProperty('service')
