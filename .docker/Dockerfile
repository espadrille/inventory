# Utiliser une image de base
FROM python:3.11-slim

# Copier les fichiers dans le conteneur
COPY inventory /inventory
COPY inventory.py /
COPY requirements.txt /

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande de démarrage
ENV CONFIG_SOURCE config_test.json
CMD ["sh", "-c", "python inventory.py --config ${CONFIG_SOURCE}"]
