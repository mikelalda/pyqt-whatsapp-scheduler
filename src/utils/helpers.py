import pyautogui
import time
from utils.copy_doc import copy_document
from platform import system
from pywhatkit.core.core import _web 

def validate_phone_number(phone_number):
    # Validate the phone number format
    import re
    pattern = r'^\+\d{1,15}$'
    return re.match(pattern, phone_number) is not None

def format_message(message):
    # Format the message to ensure it meets any specific requirements
    return message.strip()

def schedule_time_validation(hour, minute):
    # Validate the scheduled time for sending messages
    if not (0 <= hour <= 23):
        raise ValueError("Hour must be between 0 and 23.")
    if not (0 <= minute <= 59):
        raise ValueError("Minute must be between 0 and 59.")
    return True

def log_error(error_message):
    # Log error messages to a file or console
    with open('error_log.txt', 'a') as log_file:
        log_file.write(f"{error_message}\n")


def send_document(
    receiver: str,
    path: str,
    caption: str = "",
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 20
) -> None:
    """
    Sends a document to a receiver by copying it to the clipboard and pasting it.
    """
    # 1. Open WhatsApp Web to the specified receiver
    _web(receiver=receiver, message="")
    time.sleep(wait_time)

    # 2. Copy the document to the system clipboard
    print("Copying document to clipboard...")
    copy_document(path)
    print("Document copied.")
    
    # 3. Paste the document into the chat
    # This action will open the WhatsApp "Send File" preview screen
    print("Pasting document...")
    if system().lower() == "darwin":
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")
    time.sleep(10) # Wait for the preview dialog to appear

    # 4. Type the caption, if one is provided
    if caption:
        print("Typing caption...")
        pyautogui.write(caption)
        time.sleep(1)

    # 5. Press Enter/Return to send the document
    print("Sending document...")
    if system().lower() == "darwin":
        pyautogui.press("return")
    else:
        pyautogui.press("enter")
    
    print("Document sent successfully!")
    time.sleep(close_time)

    # 6. Close the tab if requested
    if tab_close:
        if system().lower() == "darwin":
            pyautogui.hotkey("command", "w")
        else:
            pyautogui.hotkey("ctrl", "w")