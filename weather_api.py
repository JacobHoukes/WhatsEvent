import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(location, date, hour):
    """
    Get weather forecast for a specific location, date and hour.

    Args:
        location (str): City name
        date (str): Date in YYYY-MM-DD format
        hour (str): Hour in 0-23 format

    Returns:
        str: Formatted weather information
    """
    if not (0 <= int(hour) <= 23):
        print("Invalid hour; please enter a number between 0 and 23.")
        exit()

    API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=3&aqi=no&alerts=no"

    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            weather_data = response.json()

            forecast_days = weather_data['forecast']['forecastday']
            forecast_for_date = next((day for day in forecast_days if day["date"] == date), None)
            if forecast_for_date:
                hour_data = forecast_for_date["hour"]
                selected_hour = next((h for h in hour_data if h["time"].endswith(f" {hour}:00")), None)

                if selected_hour:
                    location = weather_data['location']['name']
                    country = weather_data['location']['country']
                    temperature_c = selected_hour['temp_c']
                    condition = selected_hour['condition']['text']
                    return f"""
        Weather in {location}, {country} on {date} at {hour}:00 :
        
        🌡️ Temperature: {temperature_c}°C
        ⛅ Condition: {condition}
        
        """
                else:
                    return f"No weather data available for {date} at {hour}:00."
            else:
                return f"No forecast data available for {date}."
        else:
            return "Error:", response.status_code
    except requests.RequestException as e:
        return "Request failed:", e