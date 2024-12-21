import pg8000
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

def connect():
    """Fonction pour se connecter à la base de données PostgreSQL avec pg8000"""
    try:
        # Paramètres de connexion
        conn = pg8000.connect(
            user="postgres",  # Nom d'utilisateur (par défaut 'postgres')
            password=os.getenv("POSTGRES_PASSWORD", "ericona"),  # Mot de passe (par défaut 'erico')
            host="localhost",  # Hôte local
            port=5432,  # Port PostgreSQL par défaut
            database="meteo_db"  # Nom de la base de données
        )
        return conn
    except Exception as e:
        print(f"Erreur : impossible de se connecter à la base de données. {e}")
        return None
