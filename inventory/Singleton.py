"""
    classe Singleton (une seule instanciation de cette classe est possible)
"""

class Singleton():
    """
        classe Singleton (une seule instanciation de cette classe est possible)
    """

    __instance = None

    #
    # Private methods
    #
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
