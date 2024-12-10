# Pipeline-de--donnees-Meteo-Dakar-Thies

## Description
Ce projet scrappe quotidiennement les données météo des villes de Dakar et Thiès depuis l'API OpenWeather et les stocke dans une base de données PostgreSQL. Un tableau de bord permet de visualiser les données via Power BI ou Looker Studio.

## Fonctionnalités
- Récupération des données météo : ville, température, description météo, pression, humidité, timestamp.
- Stockage des données dans une base PostgreSQL via Docker.
- API Flask pour lancer manuellement l'extraction des données.

## Configuration
### Prérequis
- Docker et Docker Compose
- Compte sur OpenWeather pour obtenir une clé API.

### Commandes
1. Démarrer les services :
   ```bash
   docker-compose up --build
