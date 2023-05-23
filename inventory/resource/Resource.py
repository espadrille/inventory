#
# Classe Resource
#
class Resource:
    id :str
    name :str
    description :str

    def __init__(self, id: str, name: str=""):
        self.id = id
        self.name = name
        if name == "":
            self.name = self.id.upper()
        self.description = ""

    def print(self):
        print(self.id)
        print(f"    name                : {self.name}")
        print(f"    description         : {self.description}")
