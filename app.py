from WhatsEvent.whatsapp_api import send_message
from weather_api import get_weather
from events_api import print_events_by_city
from whatsapp_api import get_or_create_conversation, return_latest_message, add_participant, list_messages
import time

def get_user_input():
    # Change to get inputs from Whatsapp
    LOCATION = input("Please enter the name of your city: ")
    DATE = input("Enter the date (YYYY-MM-DD): ")
    HOUR = input("Enter the hour (0-23): ")
    return LOCATION, DATE, HOUR



def create_response(location, date, hour):
    event_message = print_events_by_city(location, country_code="DE", page_size=10, classification="sports") #Refactor Classification!!!
    weather_message = get_weather(location, date, hour)
    try:
        message = event_message + weather_message
        return message
    except TypeError as t:
        print(f"Error: {t}")
    except UnboundLocalError as u:
        print(u)


def manage_conversation(messages):
    pass

from listening import write_file
def main_test():

    print("Starting Weather & Events WhatsApp Bot...")
    # 1. Get or Create a Conversation:
    conversation_sid = get_or_create_conversation()

    # 2. Add or Confirm Participant to the Conversation:
    participant_sid = add_participant(conversation_sid)

    # 3. send_welcome_message -> pending!
    send_message(conversation_sid, message="Welcome to WhatsEvents-Bot! Please provide your city and the date you want to go out: (e.g.: 'Berlin, 2025-04-04, 18')")
    # write_file() (append messages with message)

    # 4. Validate User Input -> pending!
    print(return_latest_message(conversation_sid))
    welcome_message = return_latest_message(conversation_sid)


    while True:
        time.sleep(10) # Check only every 10 seconds
        new_message = return_latest_message(conversation_sid)

        if new_message.lower() == "stop":
            break

        elif new_message != welcome_message:
            city, date, hour = new_message.split(",")
            response = create_response(city, date, hour)

            # validation -> messages, state, ...
            # write JSON

            # Pass new_message to APIs:
            # Define Message
            send_message(conversation_sid, message=response)
            send_message(conversation_sid, message="")


def main():
    print("Starting Weather & Events WhatsApp Bot...")
    # 1. Get or Create a Conversation:
    conversation_sid = get_or_create_conversation()

    # 2. Add or Confirm Participant to the Conversation:
    participant_sid = add_participant(conversation_sid)

    # 3. send_welcome_message
    send_message(conversation_sid,
                 message="Welcome to WhatsEvents-Bot! Please provide your city and the date you want to go out: (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service.")

    # Store the welcome message
    last_processed_message = return_latest_message(conversation_sid)

    # Main service loop
    while True:
        time.sleep(10)  # Check only every 10 seconds
        new_message = return_latest_message(conversation_sid)

        # Skip if no new message or same as last processed
        if new_message == last_processed_message:
            continue

        # Check for stop command
        if new_message.lower().strip() == "stop":
            send_message(conversation_sid, message="Thank you for using WhatsEvents-Bot! The service has been stopped.")
            break

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
            if return_latest_message(conversation_sid) == "Sorry, I couldn't understand that format. Please provide your city, date, and hour separated by commas (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service.":
                continue
            else:
                send_message(conversation_sid,
                         message="Sorry, I couldn't understand that format. Please provide your city, date, and hour separated by commas (e.g.: 'Berlin, 2025-04-04, 18') or type 'stop' to end the service.")

        # Update the last processed message
        last_processed_message = new_message

if __name__ == "__main__":
    main()