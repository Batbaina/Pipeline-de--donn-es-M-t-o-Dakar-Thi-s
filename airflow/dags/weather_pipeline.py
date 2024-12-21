from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from app.app import crawl

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),  # Retry delay for failed tasks
}

# Define the DAG
dag = DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Pipeline for weather data extraction every two hours',
    schedule_interval='*/2 * * * *',  # Schedule: every 2 hours
    start_date=datetime(2024, 12, 1),  # Replace with your desired start date
    catchup=False,
)

# Define the task
task_fetch_weather = PythonOperator(
    task_id='crawl',
    python_callable=crawl,
    dag=dag,
)
