import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Ticketmaster API Key
API_KEY = os.getenv("API_KEY_EVENT")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def print_events_by_city(city, country_code="DE", keyword=None, classification=None, page_size=10):
    """
    Search for events by city and return formatted event information.

    Args:
        city (str): City name to search for events
        country_code (str, optional): Country code. Defaults to "DE".
        keyword (str, optional): Event keyword for filtering. Defaults to None.
        classification (str, optional): Event classification for filtering. Defaults to None.
        page_size (int, optional): Number of events to return. Defaults to 10.

    Returns:
        str: Formatted string containing event information
    """
    params = {
        "city": city,
        "countryCode": country_code,
        "apikey": API_KEY,
        "size": page_size,
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

        found_events = f"🎉 {len(events)} Events in {city}, {country_code}:\n"

        for event in events:
            # Extract event details
            name = event.get('name', 'N/A')
            start_time = event.get('dates', {}).get('start', {}).get('dateTime', 'Unknown Date')
            if start_time != "Unknown Date":
                start_time = start_time.replace("T", ", starting at ").replace("Z", "")
            event_url = event.get('url', 'N/A')
            event_type = (
                event['classifications'][0]['segment']['name'],
                event['classifications'][0]['genre']['name']
            )

            # Extract venue details
            venue_name = event.get('_embedded', {}).get('venues', [{}])[0].get('name', '')
            city_name = event.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name', 'Unknown City')
            address = event.get('_embedded', {}).get('venues', [{}])[0].get('address', {}).get('line1',
                                                                                               'Unknown Address')
            postal_code = event.get('_embedded', {}).get('venues', [{}])[0].get('postalCode', 'Unknown Postal Code')

            # Format the event details into a string
            found_events += f"""
        🔹 **{name}**
        📅 Date: {start_time}
        📍 Location: {venue_name} - {address}, {city_name}, {postal_code}
        🎭Event Type: {event_type}
        🔗 Event Link: {event_url}
        
            """
        return found_events # Remove trailing whitespace

    except requests.exceptions.RequestException as e:
        return f"❌ API Request Failed: {e}"