import os
import json
from datetime import datetime

JSON_FILE = "participants.json"

# Save phone number to JSON file
def read_file():
    data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    return data


def write_file(conversation_sid, phone_num):
    """Update participant's information in the JSON file."""
    data = read_file()
    data[conversation_sid] = phone_num
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)
            print(f"File ({JSON_FILE}) successfully written")
    except FileNotFoundError as f:
        print(f"ERROR found: {f}")


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

