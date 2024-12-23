import pg8000
import os

def connect():
    """Connect to the PostgreSQL database using pg8000."""
    try:
        conn = pg8000.connect(
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'ericona'),
            host=os.getenv('DB_HOST', 'db'),  # 'db' is the service name from docker-compose.yml
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME', 'meteo_db')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
