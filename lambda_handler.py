#!/usr/bin/python3
"""
Ce script propose un code python pour declencher l'inventaire depuis une focntion Lambda sur AWS
"""

import os
from inventory.Inventory import Inventory


def lambda_handler(event, context):
    """Declencheur de l'inventaire dans AWS Lambda

    Args:
        event : evennement recu par la fonction Lambda
        context : contexte de la fonction Lambda
    """

    # Recuperer la source de configuration
    if 'config_source' in event:
        config_source = event['config_source']
    elif 'config_source' in os.environ:
        config_source = os.environ['config_source']
    else:
        config_source = ''

    my_inventory = Inventory(id="my_inventory",
                             config_source=config_source,
                             colorize=False
                            )
    my_inventory.LoadResources()
    my_inventory.Write()
    my_inventory.Print()

if __name__ == "__main__":
    lambda_handler({}, {})
