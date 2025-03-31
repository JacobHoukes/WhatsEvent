import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio credentials (DO NOT upload to GitHub!)
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY_SID = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
CHAT_SERVICE_SID = os.getenv("CONVERSATION_SERVICE_ID")

# Initialize Twilio client
client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)


# Step 1: Create a new conversation
def create_conversation():
    conversation = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.create(
        friendly_name="Hackathon Conversation"
    )
    print(f"Conversation created with SID: {conversation.sid}")
    return conversation.sid


# Step 2: Add participant (your phone number)
def add_participant(conversation_sid, phone_number):
    participant = client.conversations.v1.services(CHAT_SERVICE_SID).conversations(
        conversation_sid).participants.create(
        messaging_binding_address=phone_number,
        messaging_binding_proxy_address=os.getenv("MASTERSCHOOL_WA_NUM")
    )
    print(f"Participant added with SID: {participant.sid}")
    return participant.sid


# Step 3: Send a message to the conversation
def send_message(conversation_sid, message):
    message = client.conversations.v1.services(CHAT_SERVICE_SID).conversations(conversation_sid).messages.create(
        body=message
    )
    print(f"Message sent with SID: {message.sid}")
    return message.sid


if __name__ == "__main__":
    my_phone = os.getenv("PRIVATE_WHATSAPP_NUM")  # Replace with your WhatsApp number
    # conversation_sid = create_conversation()  # Create a new conversation
    # add_participant(conversation_sid, my_phone)
    conversation_sid = os.getenv("CONVERSATION_SID")
    send_message(conversation_sid, "Hello! This is a test message NO 2.")