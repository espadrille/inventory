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
parser.add_option("-n",
                  "--name",
                  dest="name",
                  help="Nom de l'inventaire",
                  default="par defaut"
                  )
parser.add_option("-p",
                  "--providers",
                  dest="providers",
                  help="Liste des providers a utiliser (defaut=['aws'])",
                  default=['aws']
                  )
parser.add_option("--print-resources",
                  action="store_true",
                  dest="print_resources",
                  help="Indique s'il faut afficher le detail des ressources de l'inventaire (defaut=False)",
                  default=False
                  )
(options, args) = parser.parse_args()

# Construction de l'inventaire
my_inventory = Inventory(id="my_inventory", 
                         name=options.name, 
                         providers=options.providers, 
                         config_file=options.config_file
                         )

# Valorisation de l'inventaire
my_inventory.LoadResources()

# Affichage de l'inventaire
my_inventory.Print()
if options.print_resources:
    my_inventory.PrintResources()
