from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from app import crawl  # Importation de la fonction crawl

def weather_data_task():
    """Exécute la collecte des données météo."""
    crawl()  # Appel à la fonction crawl

with DAG('weather_data_dag', start_date=datetime(2024, 12, 22), schedule_interval='@hourly') as dag:
    weather_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=weather_data_task
    )
