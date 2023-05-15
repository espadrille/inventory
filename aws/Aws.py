# Interface AWS

#
# Imports
#
from os import path
from pathlib import Path
from configparser import ConfigParser
import boto3

#
# Classe AWS
#
class Aws:
    config_file = f"{Path.home()}/.aws/config"

    sessions = {} # Liste des sessions AWS (une par profile)

    profiles = []
    services = {}

    def __init__(self):
        if path.exists(self.config_file):
            parser = ConfigParser()
            parser.read(self.config_file)
            sections = parser.sections()
            for section in sections:
                my_profile = section.split(' ')[1]
                self.profiles.append(my_profile)
        self.connect()
        self.LoadServices()

    def connect(self):
        for profile in self.profiles:
            try:
                self.sessions[profile] = boto3.Session(profile_name=profile)
            except:
                print(f"Impossible de se connecter sur le profile {profile}")

    def LoadService(self, service_name):
        if service_name == "ec2":
            from .ec2.Ec2 import Ec2
            for profile in self.profiles:
                self.services[f"{service_name}_{profile}"] = Ec2(session=self.sessions[profile], name=f"ec2_{profile}")

    def LoadServices(self, service_names=["ec2"]):
        for service_name in service_names:
            self.LoadService(service_name=service_name)

    def print(self):
        print("======= profiles")
        for profile in self.sessions:
            print(profile)
        print("======= services")
        for k_service, service in self.services.items():
           service.print()

