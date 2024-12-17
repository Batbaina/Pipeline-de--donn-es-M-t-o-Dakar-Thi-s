from models.connect import connect
from flask import jsonify
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

def crawl():
    conn = connect()
    data = []
    if conn is not None:
        occurences = []
        api_key = os.getenv('api_key')
        lat = 14.6937
        lon = -17.444059
        # start = 1369789200
        # end = 1629233600
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            list_data = data['list']
            ville = data["city"]["name"]
            for datum in list_data:
                temp = int(datum["main"]["temp"] - 273.75)
                timestamp = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
                occurence = {
                    timestamp :{
                    "name": ville,  # Access the first element
                    "temperature": temp,
                    "description": datum["weather"][0]["description"],
                    "pression": datum["main"]["pressure"],
                    "humidity": datum["main"]["humidity"]
                    }
                }
                insert(occurence)
                
                occurences.append(occurence)
            
            return occurences
        else:
            data = f"Problems with API response {response.status_code}"
    else:
       data = "Problems with Database"
    
    return data

def insert(data):
    conn = connect()
    if conn is not None:
        cur = conn.cursor()
        for timestamp, weather_data in data.items():
            cur.execute("INSERT INTO meteo (timestamp, ville, temperature, description, pression, humidite) VALUES (%s, %s, %s, %s, %s, %s)", (timestamp, weather_data["name"], weather_data["temperature"], weather_data["description"], weather_data["pression"], weather_data["humidity"]))
        conn.commit()
        cur.close()
        conn.close()
    else:
        print("Database connection failed")