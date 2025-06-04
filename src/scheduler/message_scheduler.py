from datetime import datetime


class MessageScheduler:
    def __init__(self):
        self.scheduled_messages = []

    def schedule_message(self, user, message, time):
        self.scheduled_messages.append({
            'user': user,
            'message': message,
            'time': time,
            'sent': False
        })

    def get_scheduled_messages(self):
        return self.scheduled_messages

    def clear_scheduled_messages(self):
        self.scheduled_messages.clear()

    def remove_message(self, index):
        if 0 <= index < len(self.scheduled_messages):
            del self.scheduled_messages[index]

    def edit_message(self, index, user, message, time):
        if 0 <= index < len(self.scheduled_messages):
            self.scheduled_messages[index].update({
                'user': user,
                'message': message,
                'time': time,
                'sent': False
            })

    def mark_as_sent(self, index):
        if 0 <= index < len(self.scheduled_messages):
            self.scheduled_messages[index]['sent'] = True

    def remove_sent_messages(self):
        self.scheduled_messages = [msg for msg in self.scheduled_messages if not msg.get('sent', False)]