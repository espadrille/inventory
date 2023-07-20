#!/usr/bin/python3

# Import des modules
from inventory import *
from optparse import OptionParser

# Lecture des arguments d'appel
parser = OptionParser()
parser.add_option("-f",
                  "--config-file",
                  dest="config_file",
                  help="Chemin complet du fichier de configuration au format json (defaut=config.json)",
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
                         config_file=options.config_file
                         )

# Valorisation de l'inventaire
my_inventory.LoadResources()
my_inventory.Output()

# Affichage de l'inventaire
if options.show_resources:
    my_inventory.PrintResources()
elif options.list_resources:
    my_inventory.ListResources()
else:
    my_inventory.Print()

