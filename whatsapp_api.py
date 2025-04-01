import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio credentials
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY_SID = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
CHAT_SERVICE_SID = os.getenv("CONVERSATION_SERVICE_ID")
MY_PHONE = os.getenv("PRIVATE_WHATSAPP_NUM")  # Your WhatsApp number
MASTERSCHOOL_WA_NUM = os.getenv("MASTERSCHOOL_WA_NUM")  # Twilio proxy number

# Initialize Twilio client
client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def get_conversation_resource(conversation_sid=None):
    """Get the conversation resource for a given SID or the base conversation resource"""
    base_resource = client.conversations.v1.services(CHAT_SERVICE_SID).conversations
    return base_resource(conversation_sid) if conversation_sid else base_resource


def list_messages(conversation_sid):
    """Fetch and print all messages in a conversation."""
    messages = get_conversation_resource(conversation_sid).messages.list()

    if not messages:
        print("No messages found in the conversation.")
        return

    print(f"Messages in conversation {conversation_sid}:")
    for msg in messages:
        print(f"[{msg.date_created}] {msg.author}: {msg.body}")


def list_participants(conversation_sid):
    """Fetch and print all participants in a conversation."""
    participants = get_conversation_resource(conversation_sid).participants.list()

    if not participants:
        print("No participants found in the conversation.")
        return

    print(f"Participants in conversation {conversation_sid}:")
    for p in participants:
        address = p.messaging_binding.get("address", "N/A") if p.messaging_binding else "N/A"
        print(f"- Participant SID: {p.sid}, Address: {address}")


def list_conversations():
    """ Fetch all existing conversations and return as a list. """
    print("Fetching existing conversations...\n")
    conversations = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.list()

    if not conversations:
        print("No conversations found.")
    else:
        for conv in conversations:
            print(f"SID: {conv.sid} | Name: {conv.friendly_name} | State: {conv.state}")

    return conversations


def get_or_create_conversation():
    """ Get an existing conversation or create a new one if none exist. """
    conversations = list_conversations()

    # If a conversation already exists, return its SID
    if conversations:
        print("Using existing conversation.")
        return conversations[0].sid

    # If no conversation exists, create one
    print("Creating a new conversation...")
    conversation = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.create(
        friendly_name="Hackathon Conversation"
    )
    print(f"Created new conversation with SID: {conversation.sid}")
    return conversation.sid


def add_participant(conversation_sid):
    """ Add a participant (your WhatsApp number) to the conversation if not already present """
    participants = get_conversation_resource(conversation_sid).participants.list()

    #check if your phone number is already a participant
    your_participant = None
    for p in participants:
        if p.messaging_binding and p.messaging_binding.get("address") == MY_PHONE:
            your_participant = p
            break

    if your_participant:
        print(f"Your number ({MY_PHONE}) is already a participant.")
        return your_participant.sid

    # prints all participants if they exist
    if participants:
        print(f"Participants in conversation {conversation_sid}:")
        for p in participants:
            address = p.messaging_binding.get("address", "N/A" if p.messaging_binding else "N/A")
            print(f"- Participant SID: {p.sid}, Address: {address}")

    # add new participant
    print(f"Adding participant ({MY_PHONE}) to conversation {conversation_sid}...")
    participant = get_conversation_resource(conversation_sid).participants.create(
        messaging_binding_address=MY_PHONE,
        messaging_binding_proxy_address=MASTERSCHOOL_WA_NUM
    )
    print(f"Participant added with SID: {participant.sid}")
    return participant.sid


def send_message(conversation_sid, message):
    """ Send a message to the given conversation. """
    print(f"Sending message to conversation {conversation_sid}...")
    message = get_conversation_resource(conversation_sid).messages.create(
        body=message
    )
    print(f"Message sent with SID: {message.sid}")
    return message.sid


def main():
    # Print credentials for debugging
    print(f"ACCOUNT_SID: {ACCOUNT_SID}")
    print(f"API_KEY_SID: {API_KEY_SID}")
    print(f"CHAT_SERVICE_SID: {CHAT_SERVICE_SID}")

    # Get or create a conversation
    conversation_sid = get_or_create_conversation()

    # List messages in latest conversation
    list_messages(conversation_sid)

    # List participants in latest conversation
    list_participants(conversation_sid)

    # Add participant if needed
    add_participant(conversation_sid)

    # Send a test message
    send_message(conversation_sid, "Hello! This is a test message from our refactored script.")


if __name__ == "__main__":
    main()
