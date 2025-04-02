from WhatsEvent.whatsapp_api import send_message
from weather_api import print_weather
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
    weather_message = print_weather(location, date, hour)
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
def main():

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

        if new_message != welcome_message:
            city, date, hour = new_message.split(",")
            response = create_response(city, date, hour)

            # validation -> messages, state, ...
            # write JSON

            # !!! Pass new_message to APIs !!!
            # Define Message
            send_message(conversation_sid, message=response)
            break

    # User-Response:

    # Validation

    # 3. Get the latest messages, & use the latest message to design the response.

    # 4. Start/Continue Conversation -> Listening Function


    # 5. If new:
    #   send_welcome_message()
    # Else:
    #   Get user input
    #   send_message(get_or_create_conversation, message=create_message)

    # validate input and send data to API for saving and processing




    # whatsapp_response = create_message()
    # send_message(get_or_create_conversation(), message=whatsapp_response)


if __name__ == "__main__":
    main()