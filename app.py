from whatsapp_api import send_message
from weather_api import get_weather
from events_api import print_events_by_city
from data import read_file
from whatsapp_api import get_or_create_conversation, return_latest_message, add_participant, return_latest_author
import time


def get_user_input():
    """
    Get user input for location, date and hour.
    Currently using console input, to be replaced with WhatsApp input.

    Returns:
        tuple: (location, date, hour)
    """
    location = input("Please enter the name of your city: ")
    date = input("Enter the date (YYYY-MM-DD): ")
    hour = input("Enter the hour (0-23): ")
    return location, date, hour


def create_response(location, date, hour):
    """
    Create a response with event and weather information for a specified location, date and hour.

    Args:
        location (str): City name
        date (str): Date in YYYY-MM-DD format
        hour (str): Hour in 0-23 format

    Returns:
        str: Combined message with events and weather information
    """
    event_message = print_events_by_city(location, country_code="DE", page_size=10, classification="sports")
    weather_message = get_weather(location, date, hour)
    try:
        message = weather_message + event_message
        return message
    except TypeError as t:
        print(f"Error: {t}")
    except UnboundLocalError as u:
        print(u)


def main():
    """
    Main function that runs the WhatsApp bot for weather and events information.
    """
    print("Starting Weather & Events WhatsApp Bot...")
    # 1. Get or Create a Conversation:
    json_data = read_file()
    conversation_sid = get_or_create_conversation(json_data)

    # 2. Add or Confirm Participant to the Conversation:
    participant_sid = add_participant(conversation_sid)

    # 3. Send welcome message
    welcome_message = "Welcome to WhatsEvents-Bot! Please provide your city and the date you want to go out: (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service."
    send_message(conversation_sid, message=welcome_message)

    # Store the welcome message
    last_processed_message = return_latest_message(conversation_sid)

    # Main service loop
    while True:
        time.sleep(10)  # Check only every 10 seconds
        new_message = return_latest_message(conversation_sid)
        new_message_author = return_latest_author(conversation_sid)

        # Skip if no new message or same as last processed
        if new_message == last_processed_message:
            continue

        # Check for stop command
        if new_message.lower().strip() == "stop":
            send_message(conversation_sid, message="Thank you for using WhatsEvents-Bot! The service has been stopped.")
            break

        if new_message_author != "system":
            try:
                # Process the message
                city, date, hour = new_message.split(",")
                city = city.strip()
                date = date.strip()
                hour = hour.strip()

                response = create_response(city, date, hour)
                send_message(conversation_sid, message=response)

                # Add prompt for next query
                time.sleep(1)
                send_message(conversation_sid,
                             message="You can provide another city and date or type 'stop' to end the service. (e.g.: 'Berlin, 2025-04-04, 18')")

            except ValueError:
                # Handle incorrect format
                if return_latest_message(
                        conversation_sid) == "Sorry, I couldn't understand that format. Please provide your city, date, and hour separated by commas (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service.":
                    continue
                else:
                    send_message(conversation_sid,
                                 message="Sorry, I couldn't understand that format. Please provide your city, date, and hour separated by commas (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service.")

        # Update the last processed message
        last_processed_message = new_message


if __name__ == "__main__":
    main()