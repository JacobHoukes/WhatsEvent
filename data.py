import os
import json

JSON_FILE = "participants.json"


def read_file():
    """
    Read the participants data from JSON file.

    Returns:
        dict: Dictionary containing conversation SIDs and phone numbers
    """
    data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    return data


def write_file(conversation_sid, phone_num):
    """
    Update participant's information in the JSON file.

    Args:
        conversation_sid (str): The conversation SID to save
        phone_num (str): The phone number to associate with the conversation
    """
    data = read_file()
    data[conversation_sid] = phone_num
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)
            print(f"File ({JSON_FILE}) successfully written")
    except FileNotFoundError as f:
        print(f"ERROR found: {f}")