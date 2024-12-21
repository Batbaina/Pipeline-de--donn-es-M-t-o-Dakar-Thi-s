from flask import Flask, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from models.connect_db import connect

# Load environment variables
load_dotenv()

app = Flask(__name__)

def crawl():
    """Fetch weather data for cities and insert them into the database."""
    conn = connect()
    if conn is None:
        return jsonify({"error": "Database connection problem."})

    api_key = os.getenv('api_key')
    if not api_key:
        return jsonify({"error": "API key not defined in .env file."})

    # Coordinates of cities to collect
    villes = [
        {"name": "Dakar", "lat": 14.6937, "lon": -17.444059},
        {"name": "Thiès", "lat": 14.7996, "lon": -16.9310}
    ]

    occurences = []

    for ville in villes:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={ville['lat']}&lon={ville['lon']}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Process API response
            data = response.json()
            list_data = data['list']

            for datum in list_data:
                temp = int(datum["main"]["temp"] - 273.15)  # Convert temperature to Celsius
                timestamp = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
                occurence = {
                    timestamp: {
                        "name": ville["name"],
                        "temperature": temp,
                        "description": datum["weather"][0]["description"],
                        "pression": datum["main"]["pressure"],
                        "humidity": datum["main"]["humidity"],
                    }
                }
                insert(occurence)  # Insert into the database
                occurences.append(occurence)

        except requests.exceptions.RequestException as e:
            print(f"API request error for {ville['name']}: {e}")
        except KeyError as e:
            print(f"Data error for {ville['name']}: Missing key {e}")

    return jsonify(occurences)

def insert(data):
    """Insert weather data into the database."""
    conn = connect()
    if conn is None:
        print("Database connection problem.")
        return

    try:
        cur = conn.cursor()

        for timestamp, weather_data in data.items():
            cur.execute(
                """
                INSERT INTO meteo (timestamp, ville, temperature, description, pression, humidite)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    timestamp,
                    weather_data["name"],
                    weather_data["temperature"],
                    weather_data["description"],
                    weather_data["pression"],
                    weather_data["humidity"],
                ),
            )
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Data insertion error: {e}")
    finally:
        conn.close()

@app.route('/')
def fetch_weather():
    """Flask route to fetch weather data."""
    data = crawl()
    return data

if __name__ == '__main__':
    app.run(port=1000, debug=True)
