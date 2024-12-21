# Utiliser une image Python de base
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Commande par défaut
CMD ["python", "app.py"]
