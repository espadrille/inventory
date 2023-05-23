# Instance EC2

#
# Imports
#
import boto3
from ...AwsResource import AwsResource

#
# Classe Instance
#
class SecurityGroup(AwsResource):
    type = ""
    vpc_id = ""

    def __init__(self, security_group: dict, client: boto3.client.__class__):
        super().__init__(id=security_group['GroupId'], name=security_group['GroupName'], client=client)
        self.vpc_id = security_group['VpcId']

    def _get_tags(self, client: boto3.client.__class__):
        Tags :list
        try:
            Tags = client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [self.id]}])['Tags']
        except:
            Tags = []
        return Tags
        
    def print(self):
        super().print()
        print(f"    id                  : {self.id}")
        print(f"    name                : {self.name}")
        print(f"    vpc_id              : {self.vpc_id}")
        