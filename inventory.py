#!/usr/bin/python3

"""
Point d'entree du script d'inventaire
"""

# Import des modules
from inventory.Inventory import Inventory
from optparse import OptionParser

# Lecture des arguments d'appel
parser = OptionParser()
parser.add_option("-f",
                  "--config",
                  dest="config",
                  help="Emplacement de la configuration de l'inventaire au format json (defaut=config.json)",
                  default="config.json"
                  )
parser.add_option("--list-resources",
                  action="store_true",
                  dest="list_resources",
                  help="Indique s'il faut lister les ressources de l'inventaire (defaut=False)",
                  default=False
                  )
parser.add_option("--show-resources",
                  action="store_true",
                  dest="show_resources",
                  help="Indique s'il faut afficher le detail des ressources de l'inventaire (defaut=False)",
                  default=False
                  )
(options, args) = parser.parse_args()

# Construction de l'inventaire
my_inventory = Inventory(id="my_inventory", 
                         config_source=options.config
                         )

# Valorisation de l'inventaire
my_inventory.LoadResources()
# Ecriture du resultat
my_inventory.Write()

# Affichage de l'inventaire
my_inventory.Print()
if options.list_resources:
    my_inventory.ListResources()
if options.show_resources:
    my_inventory.ShowResources()
