#!/usr/bin/python3

import os
from inventory.Inventory import Inventory

def lambda_handler(event, context):
    my_inventory = Inventory(id="my_inventory", 
                         config_source=os.environ['CONFIGURATION'],
                         colorize=False
                         )
    my_inventory.LoadResources()
    my_inventory.Write()
    my_inventory.Print()

if __name__ =="__main__":
    lambda_handler({}, {})