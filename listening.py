import os
import json
from datetime import datetime

JSON_FILE = "participants.json"

# Save phone number to JSON file
def read_file(phone_number):
    data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    return data


# Save Participant in JSON FIle: Number, Message, Participant_ID, Date
def write_file(phone_number, messages, state, location, date):
    """Update participant's information in the JSON file."""
    data = read_file(phone_number)

    if phone_number in data:
        # Update existing participant
        data[phone_number]['messages'] = messages
        data[phone_number]['state'] = state
        data[phone_number]['location'] = location
        data[phone_number]['date'] = date
        print("Data updated successfully.")
    else:
        # Add new participant
        data[phone_number] = {
            "messages": messages,
            "state": state,
            "location": location,
            "date": date,
            "hour": None,  # Keeping this based on your example structure
        }
        print("New participant added.")

    try:
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)
            print(f"File ({file}) successfully written")
    except FileNotFoundError as f:
        print(f"ERROR found: {f}")
    return data

# Auto-reply function
def auto_reply(client, conversation_sid, phone_number):
    reply_message = "Welcome to Masterschool! How can we assist you today?"
    send_message(client, conversation_sid, reply_message)
    read_file(phone_number)


# Send a message function
def send_message(client, conversation_sid, message):
    conversation = client.conversations.v1.services(conversation_sid).conversations
    conversation(conversation_sid).messages.create(body=message)
    print("Message sent.")

