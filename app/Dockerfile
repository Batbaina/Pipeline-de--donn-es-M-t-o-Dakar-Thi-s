# Utilisation de l'image Python
FROM python:3.9

# Configuration du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Commande pour démarrer l'application
CMD ["python", "app.py"]
