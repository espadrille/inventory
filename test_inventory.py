#!//usr/bin/python3

# Teste de la classe Inventory
from inventory import *

my_inventory = Inventory(id="aws", name="AWS", providers=["AWS"], config_file="config.json")

my_inventory.LoadResources()

my_inventory.print()
# my_inventory.PrintResources()
