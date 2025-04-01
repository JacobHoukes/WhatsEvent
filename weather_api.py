import requests
import json

# Replace with your WeatherAPI key
API_KEY = "cab41e07e0b2476d93f202352253103"
LOCATION = "London"
API_URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"

try:
    # Send GET request
    response = requests.get(API_URL)

    # Check for successful response
    if response.status_code == 200:
        weather_data = response.json()

        # Extract and display relevant information
        location = weather_data['location']['name']
        country = weather_data['location']['country']
        temperature_c = weather_data['current']['temp_c']
        condition = weather_data['current']['condition']['text']

        print(f"Weather in {location}, {country}")
        print(f"Temperature: {temperature_c}°C")
        print(f"Condition: {condition}")
    else:
        print("Error:", response.status_code)
except requests.RequestException as e:
    print("Request failed:", e)
