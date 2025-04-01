from weather_api import print_weather
from events_api import print_events_by_city
from whatsapp_api import get_or_create_conversation, send_message

def get_user_input():
    # Change to get inputs from Whatsapp
    LOCATION = input("Please enter the name of your city: ")
    DATE = input("Enter the date (YYYY-MM-DD): ")
    HOUR = input("Enter the hour (0-23): ")
    return LOCATION, DATE, HOUR



def create_message():
    location, date, hour = get_user_input()

    weather_message = print_weather(location, date, hour)
    event_message = print_events_by_city(location)

    return weather_message + event_message


def main():

    whatsapp_response = create_message()
    send_message(get_or_create_conversation(), message=whatsapp_response)


    # print_events_by_city(location)


if __name__ == "__main__":
    main()