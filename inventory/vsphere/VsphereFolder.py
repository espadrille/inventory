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
        super().__init__()

        self.SetProperty('Name', )

        console.Debug(f"Creation client : {self.Name()}")

    #
    # Public methods
    #
    def Client(self):
        return self._client
    
    def Name(self):
        return f"{self.GetProperty('service')}.{self.GetProperty('profile')}.{self.GetProperty('region')}"
    
    def Profile(self):
        return self.GetProperty('profile')

    def Region(self):
        return self.GetProperty('region')

    def Service(self):
        return self.GetProperty('service')
