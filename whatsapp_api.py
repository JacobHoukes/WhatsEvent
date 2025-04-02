import os
from dotenv import load_dotenv
from twilio.rest import Client
from data import write_file

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


def get_conversations_list_resource(conversation_sid=None):
    """
    Get the resource for listing conversations, or a specific conversation if SID is provided.

    Args:
        conversation_sid (str, optional): The conversation SID. Defaults to None.

    Returns:
        Resource: Twilio conversations list resource
    """
    conversations_list = client.conversations.v1.services(CHAT_SERVICE_SID).conversations
    return conversations_list(conversation_sid) if conversation_sid else conversations_list


def list_messages(conversation_sid):
    """
    Fetch and print the last 5 messages in a conversation.

    Args:
        conversation_sid (str): The conversation SID

    Returns:
        list: List of message objects
    """
    messages = get_conversations_list_resource(conversation_sid).messages.list()

    if not messages:
        print("No messages found in the conversation.")
        return

    print(f"Last 5 messages in conversation {conversation_sid}:")
    for msg in messages:
        print(f"[{msg.date_created}] {msg.author}: {msg.body}")
    return messages


def return_latest_author(conversation_sid):
    """
    Get the author of the latest message in a conversation.

    Args:
        conversation_sid (str): The conversation SID

    Returns:
        str: Author of the latest message
    """
    messages = get_conversations_list_resource(conversation_sid).messages.list()
    author = messages[-1].author
    return author


def return_latest_message(conversation_sid):
    """
    Get the body of the latest message in a conversation.

    Args:
        conversation_sid (str): The conversation SID

    Returns:
        str: Body of the latest message
    """
    messages = get_conversations_list_resource(conversation_sid).messages.list()
    latest_message = messages[-1].body
    return latest_message


def list_participants(conversation_sid):
    """
    Fetch and print all participants in a conversation.

    Args:
        conversation_sid (str): The conversation SID
    """
    participants = get_conversations_list_resource(conversation_sid).participants.list()

    if not participants:
        print("No participants found in the conversation.")
        return

    print(f"Participants in conversation {conversation_sid}:")
    for p in participants:
        address = p.messaging_binding.get("address", "N/A") if p.messaging_binding else "N/A"
        print(f"- Participant SID: {p.sid}, Address: {address}")


def list_conversations():
    """
    Fetch all existing conversations and return as a list.

    Returns:
        list: List of conversation objects
    """
    print("Fetching existing conversations...\n")
    conversations = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.list()

    if not conversations:
        print("No conversations found.")
    else:
        for conv in conversations:
            print(f"SID: {conv.sid} | Name: {conv.friendly_name} | State: {conv.state}")

    return conversations


def get_or_create_conversation(json_data):
    """
    Get an existing conversation or create a new one if none exist.

    Args:
        json_data (dict): Dictionary containing conversation SIDs and phone numbers

    Returns:
        str: Conversation SID
    """
    conversations = list_conversations()

    for conversation in conversations:
        for key, value in json_data.items():
            if conversation.sid == key and MY_PHONE == value:
                return conversation.sid

    # If no conversation exists above, create one
    print("Creating a new conversation...")
    conversation = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.create(
        friendly_name="Hackathon Conversation"
    )
    print(f"Created new conversation with SID: {conversation.sid}")
    write_file(conversation.sid, MY_PHONE)
    return conversation.sid


def delete_all_conversations():
    """
    Delete all existing conversations.
    """
    conversations = client.conversations.v1.services(CHAT_SERVICE_SID).conversations.list()

    if not conversations:
        print("No conversations to delete.")
        return

    for conv in conversations:
        try:
            client.conversations.v1.services(CHAT_SERVICE_SID).conversations(conv.sid).delete()
            print(f"Deleted conversation SID: {conv.sid} | Name: {conv.friendly_name}")
        except Exception as e:
            print(f"Error deleting conversation {conv.sid}: {e}")


def add_participant(conversation_sid):
    """
    Add a participant (your WhatsApp number) to the conversation if not already present.

    Args:
        conversation_sid (str): The conversation SID

    Returns:
        str: Participant SID
    """
    participants = get_conversations_list_resource(conversation_sid).participants.list()

    # check if your phone number is already a participant
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
    participant = get_conversations_list_resource(conversation_sid).participants.create(
        messaging_binding_address=MY_PHONE,
        messaging_binding_proxy_address=MASTERSCHOOL_WA_NUM
    )
    print(f"Participant added with SID: {participant.sid}")
    return participant.sid


def remove_participant(conversation_sid, participant_sid):
    """
    Remove a participant from the given conversation.

    Args:
        conversation_sid (str): The conversation SID
        participant_sid (str): The participant SID to remove
    """
    try:
        client.conversations.v1.services(CHAT_SERVICE_SID).conversations(conversation_sid).participants(
            participant_sid).delete()
        print(f"Participant {participant_sid} removed from conversation {conversation_sid}.")
    except Exception as e:
        print(f"Error removing participant {participant_sid}: {e}")


def send_message(conversation_sid, message):
    """
    Send a message to the given conversation.

    Args:
        conversation_sid (str): The conversation SID
        message (str): The message to send

    Returns:
        str: Message SID
    """
    print(f"Sending message to conversation {conversation_sid}...")
    message = get_conversations_list_resource(conversation_sid).messages.create(
        body=message
    )
    print(f"Message sent with SID: {message.sid}")
    return message.sid


def main():
    """
    Main function for testing WhatsApp API functionality.
    """
    # Print credentials for debugging
    print(f"ACCOUNT_SID: {ACCOUNT_SID}")
    print(f"API_KEY_SID: {API_KEY_SID}")
    print(f"CHAT_SERVICE_SID: {CHAT_SERVICE_SID}")

    # Testing:
    list_conversations()


if __name__ == "__main__":
    main()