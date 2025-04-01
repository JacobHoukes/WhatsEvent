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

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Check if events exist
            events = data.get('_embedded', {}).get('events', [])
            if not events:
                return f"❌ No events found in {city}, {country_code}."

            found_events = f"\n🎉 {len(events)} Events in {city}, {country_code}:\n"

            for event in events:

                # Extract event details
                name = event.get('name', 'N/A')
                start_time = event.get('dates', {}).get('start', {}).get('dateTime', 'Unknown Date')
                event_url = event.get('url', 'N/A')
                event_type = (
                event['classifications'][0]['segment']['name'], event['classifications'][0]['genre']['name'])


                # Extract venue details
                venue_name = event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Unknown Venue')
                city_name = event.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name',
                                                                                                  'Unknown City')
                address = event.get('_embedded', {}).get('venues', [{}])[0].get('address', {}).get('line1',
                                                                                                   'Unknown Address')
                postal_code = event.get('_embedded', {}).get('venues', [{}])[0].get('postalCode', 'Unknown Postal Code')


                # Format the event details into a string
                found_events += f"""
            🔹 **{name}**
            📅 Date: {start_time}
            📍 Location: {venue_name}, {address}, {city_name}, {postal_code}
            🔗 Event Link: ({event_url})
            Event Type: {event_type}
                """
            return found_events.strip()  # Remove trailing whitespace

        except requests.exceptions.RequestException as e:
            return f"❌ API Request Failed: {e}"


# Example: Get events in Los Angeles, US
# get_events_by_city(city="Chicago", country_code="US", keyword="theatre", classification="music", page_size=10)
# print(print_events_by_city(city="Cologne", country_code="DE", page_size=10, classification="sports")) # optional: add keywords and classification
