import os
import json
from datetime import datetime

JSON_FILE = "participants.json"


# Save phone number to JSON file
def save_number_to_json(phone_number):
    data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)

    if phone_number not in data:
        data[phone_number] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Number {phone_number} saved to {JSON_FILE}")
    else:
        print(f"Number {phone_number} already exists in {JSON_FILE}")

# Auto-reply function
def auto_reply(client, conversation_sid, phone_number):
    reply_message = "Welcome to Masterschool! How can we assist you today?"
    send_message(client, conversation_sid, reply_message)
    save_number_to_json(phone_number)

# Send a message function
def send_message(client, conversation_sid, message):
    conversation = client.conversations.v1.services(conversation_sid).conversations
    conversation(conversation_sid).messages.create(body=message)
    print("Message sent.")
