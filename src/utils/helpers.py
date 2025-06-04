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