# Interface AWS

#
# Imports
#
import boto3

#
# Classe AWS
#
class Aws:
    sessions = {} # Liste des sessions AWS (une par profile)

    profiles = []
    services = {}

    def __init__(self):
        self.profiles = boto3.session.Session().available_profiles

    def Connect(self):
        for profile in self.profiles:
            try:
                self.sessions[profile] = boto3.Session(profile_name=profile)
            except:
                print(f"Impossible de se connecter sur le profile {profile}")

    def LoadResources(self):
        self.LoadServices(service_names=["ec2"])

    def LoadServices(self, service_names=[]):
        for service_name in service_names:
            self.LoadService(service_name=service_name)

    def LoadService(self, service_name):
        if service_name == "ec2":
            from .ec2.Ec2 import Ec2
            for profile in self.profiles:
                self.services[f"{service_name}_{profile}"] = Ec2(session=self.sessions[profile], name=f"ec2_{profile}")

    def print(self):
        print("======= profiles")
        for profile in self.sessions:
            print(profile)
        print("======= services")
        for k_service, service in self.services.items():
           service.print()

