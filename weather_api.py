import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

LOCATION = input("Please enter the name of your city: ")
DATE = input("Enter the date (YYYY-MM-DD): ")
HOUR = input("Enter the hour (0-23): ")

if not HOUR.isdigit() or not (0 <= int(HOUR) <= 23):
    print("Invalid hour; please enter a number between 0 and 23.")
    exit()
API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=3&aqi=no&alerts=no"
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        weather_data = response.json()

        forecast_days = weather_data['forecast']['forecastday']
        forecast_for_date = next((day for day in forecast_days if day["date"] == DATE), None)
        if forecast_for_date:

            hour_data = forecast_for_date["hour"]
            selected_hour = next((h for h in hour_data if h["time"].endswith(f" {HOUR}:00")), None)
            if selected_hour:
                location = weather_data['location']['name']
                country = weather_data['location']['country']
                temperature_c = selected_hour['temp_c']
                condition = selected_hour['condition']['text']
                print(f"Weather in {location}, {country} on {DATE} at {HOUR}:00")
                print(f"Temperature: {temperature_c}°C")
                print(f"Condition: {condition}")
            else:
                print(f"No weather data available for {DATE} at {HOUR}:00.")
        else:
            print(f"No forecast data available for {DATE}.")
    else:
        print("Error:", response.status_code)
except requests.RequestException as e:
    print("Request failed:", e)
