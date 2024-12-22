# Utiliser une image officielle Python
FROM python:3.10-slim

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

COPY ./models ./models

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Exposer le port 1000 pour le conteneur
EXPOSE 1000

# Définir la commande pour exécuter l'application Flask
CMD ["python", "app.py"]
