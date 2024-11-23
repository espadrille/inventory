'''
    Module de classe AwsClient
'''

import boto3
from ..Console import console
from ..Object import Object

class AwsClient(Object):
    '''
        Classe AwsClient
    '''

    _boto3_client: boto3.client.__class__
    _boto3_session: boto3.Session

    #
    # Private methods
    #
    def __init__(self, service: str, role: tuple, region:str=""):
        super().__init__()

        (profile, role_arn) = role

        self.SetProperty('service', service)
        self.SetProperty('profile', profile)
        self.SetProperty('role_arn', role_arn)
        self.SetProperty('region', region)

        sts = boto3.client('sts')
        assumed_role_properties = sts.assume_role(RoleArn=role_arn, RoleSessionName=profile)
        self._boto3_session = boto3.Session(            # Une session par profile
            aws_access_key_id=assumed_role_properties['Credentials']['AccessKeyId'],
            aws_secret_access_key=assumed_role_properties['Credentials']['SecretAccessKey'],
            aws_session_token = assumed_role_properties['Credentials']['SessionToken']
            )

        if region == "":
            self._boto3_client = self._boto3_session.client(service_name=self.GetProperty('service')) # type: ignore
        else:
            self._boto3_client = self._boto3_session.client(service_name=self.GetProperty('service'), region_name=self.GetProperty('region')) # type: ignore

        console.Debug(f"Creation client : {self.Name()}")

    #
    # Public methods
    #
    def Client(self):
        '''
            Retourne le client
        '''
        return self._boto3_client

    def Name(self):
        '''
            Nom du client
        '''
        retour = ""
        if self.GetProperty('region') == "":
            retour = f"{self.GetProperty('service')}.{self.GetProperty('profile')}"
        else:
            retour = f"{self.GetProperty('service')}.{self.GetProperty('profile')}.{self.GetProperty('region')}"
        return retour

    def Profile(self):
        '''
            Le 'profile' de configuration du client
        '''
        return self.GetProperty('profile')

    def Region(self):
        '''
            La region du client
        '''
        return self.GetProperty('region')

    def Service(self):
        '''
            Le service du cient
        '''
        return self.GetProperty('service')
