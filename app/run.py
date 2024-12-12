from flask import Flask, jsonify
import requests
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

# Configuration for PostgreSQL
db_config = {
    "dbname": "weather_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

# OpenWeather API configuration
API_KEY = "14b54075ea18cc5e901c50f0208188ff"
CITY = "Dakar"
COUNTRY = "SN"
API_URL = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={CITY},{COUNTRY}&cnt=1&appid={API_KEY}"

# Function to initialize the database
def init_db():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city_name VARCHAR(50),
            country_code VARCHAR(10),
            temperature FLOAT,
            description TEXT,
            pressure INT,
            humidity INT,
            timestamp TIMESTAMP
        );
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Function to fetch and store weather data
def fetch_weather_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        if data and "list" in data:
            weather_entry = data["list"][0]
            city_name = data["city"]["name"]
            country_code = data["city"]["country"]
            temperature = weather_entry["temp"]["day"] - 273.15  # Convert Kelvin to Celsius
            description = weather_entry["weather"][0]["description"]
            pressure = weather_entry["pressure"]
            humidity = weather_entry["humidity"]
            timestamp = datetime.utcfromtimestamp(weather_entry["dt"])

            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO weather_data (city_name, country_code, temperature, description, pressure, humidity, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (city_name, country_code, temperature, description, pressure, humidity, timestamp))
            connection.commit()
            cursor.close()
            connection.close()

            print(f"Weather data for {city_name} added successfully.")
        else:
            print("No valid data received from the API.")

    except Exception as e:
        print(f"Error fetching weather data: {e}")

# Schedule the weather data fetching
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_weather_data, 'interval', hours=1)  # Adjust interval as needed
    scheduler.start()

@app.route('/')
def home():
    return jsonify({"message": "Weather data collection for Dakar is running."})

@app.route('/data')
def get_data():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM weather_data ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "city_name": row[1],
                "country_code": row[2],
                "temperature": row[3],
                "description": row[4],
                "pressure": row[5],
                "humidity": row[6],
                "timestamp": row[7]
            })

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    init_db()
    start_scheduler()
    app.run(debug=True)
