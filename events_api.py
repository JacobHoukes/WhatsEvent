import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Ticketmaster API Key
API_KEY = os.getenv("API_KEY_EVENT")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def get_event_for_category(city, date, hour, country_code, category, page_size=1):
    """
    Queries the Ticketmaster API for events of a specific category.
    """
    start_datetime = f"{date}T{hour}:00:00Z"
    params = {
        "city": city,
        "countryCode": country_code,
        "apikey": API_KEY,
        "size": page_size,
        "sort": "date,asc",
        "startDateTime": start_datetime,
        "classificationName": category  # Filter for the category
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    events = data.get('_embedded', {}).get('events', [])
    if events:
        return events[0]  # Return the first event found
    return None


def print_events_by_city(city, date, hour, country_code="", max_events=3):
    """
    Search for events by city and return formatted event information by directly querying each category.
    """
    # Expanded categories with icons
    categories = {
        "Music": "🎵",
        "Sports": "⚽",
        "Theatre": "🎭",
        "Comedy": "😂",
        "Arts": "🎨",
        "Film": "🎬",
        "Family": "👨‍👩‍👧‍👦",
        "Festivals": "🎉",
        "Food & Drink": "🍔",
        "Exhibitions": "🖼️"
    }

    selected_events = []

    # Query the API for each category until we have enough events.
    for category in categories:
        event = get_event_for_category(city, date, hour, country_code, category)
        if event:
            selected_events.append((category, event))
        if len(selected_events) >= max_events:
            break

    # If not enough events were found, you could decide to fill up the rest by repeating queries for popular categories.
    if not selected_events:
        return f"❌ No events found in {city}, {country_code} on {date} at {hour}:00."

    # Format the output string.
    found_events = "🎉 Here are some diverse events happening in your area:\n"
    if len(selected_events) < max_events:
        found_events += "\n⚠️ Some categories were not found, showing available events.\n"

    for event_type, event in selected_events:
        icon = categories.get(event_type, "❓")
        name = event.get('name', 'N/A')
        start_time = event.get('dates', {}).get('start', {}).get('dateTime', 'Unknown Date')
        if start_time != "Unknown Date":
            start_time = start_time.replace("T", ", starting at ").replace("Z", "")
        event_url = event.get('url', 'N/A')
        venue = event.get('_embedded', {}).get('venues', [{}])[0]
        venue_name = venue.get('name', '')
        city_name = venue.get('city', {}).get('name', 'Unknown City')
        address = venue.get('address', {}).get('line1', 'Unknown Address')
        postal_code = venue.get('postalCode', 'Unknown Postal Code')

        found_events += (
            f"\n{icon} **{name}**\n"
            f"📅 Date: {start_time}\n"
            f"📍 Location: {venue_name} - {address}, {city_name}, {postal_code}\n"
            f"🔗 Event Link: {event_url}\n"
        )

    return found_events.strip()


# Example usage:
if __name__ == "__main__":
    print(print_events_by_city("Berlin", "2025-04-04", "18", country_code="DE"))
