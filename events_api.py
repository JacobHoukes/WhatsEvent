import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Ticketmaster API Key
API_KEY = os.getenv("API_KEY_EVENT")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

# Function to search events by city
def print_events_by_city(city, country_code="DE", keyword=None, classification=None, page_size=10):
    params = {
        "city": city,
        "countryCode": country_code,
        "apikey": API_KEY,
        "size": page_size,  # Number of results per page
        "sort": "date,asc"  # Sort by earliest event first
    }

    # Optional Filters
    if keyword:
        params["keyword"] = keyword
    if classification:
        params["classificationName"] = classification

    # API Request
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Check if events exist
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            print(f"\n🎉 {len(events)} Events in {city}, {country_code}:\n")

            found_events = ""
            for event in events:
                name = event.get('name', 'N/A')
                start_time = event.get('dates', {}).get('start', {}).get('localDate', 'Unknown Date')
                venue = event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Unknown Venue')
                city_name = event.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name', 'Unknown City')
                found_events += f"""
                            🎟️ Event: {name}
                            📅 Date: {start_time}
                            📍 Location: {venue}, {city_name}/n
                        """
        else:
            found_events = f"No events found in {city}, {country_code}."
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

    return found_events


# Example: Get events in Los Angeles, US
# get_events_by_city(city="Chicago", country_code="US", keyword="theatre", classification="music", page_size=10)

# print_events_by_city(city="Cologne", country_code="DE", page_size=10, classification="sports, music") # optional: add keywords and classification
