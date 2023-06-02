#!/usr/bin/python3

# Teste de la classe Inventory
from inventory import *

my_inventory = Inventory(id="my_inventory", name="Mon inventaire", providers=["aws"], config_file="config.json")

my_inventory.LoadResources()

my_inventory.print()
# my_inventory.PrintResources()
