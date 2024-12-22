import pg8000
from models.connect_db import connect

def initialize_database():
    """Initialize the database (e.g., create tables if needed)."""
    conn = connect()
    if conn is None:
        print("Database connection problem.")
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS meteo (
                timestamp TEXT PRIMARY KEY,
                ville TEXT NOT NULL,
                temperature INTEGER,
                description TEXT,
                pression INTEGER,
                humidite INTEGER
            );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()
