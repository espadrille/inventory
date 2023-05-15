#!//usr/bin/python3

# Teste de la classe Inventory
from inventory import *

my_inventory = Inventory(provider="Aws")

my_inventory.Connect()
my_inventory.LoadResources()

my_inventory.print()
