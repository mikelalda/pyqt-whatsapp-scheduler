class MessageScheduler:
    def __init__(self):
        self.scheduled_messages = []

    def schedule_message(self, user, message, time, file_path=None):
        self.scheduled_messages.append({
            'user': user,
            'message': message, # Este será el pie de foto (caption)
            'time': time,
            'file_path': file_path, # NUEVO
            'sent': False
        })

    def get_scheduled_messages(self):
        return self.scheduled_messages

    def clear_scheduled_messages(self):
        self.scheduled_messages.clear()

    def remove_message(self, index):
        if 0 <= index < len(self.scheduled_messages):
            del self.scheduled_messages[index]

    def edit_message(self, index, user, message, time, file_path=None):
        if 0 <= index < len(self.scheduled_messages):
            self.scheduled_messages[index].update({
                'user': user,
                'message': message,
                'time': time,
                'file_path': file_path, # NUEVO
                'sent': False # Se resetea el estado a no enviado al editar
            })

    def mark_as_sent(self, index):
        if 0 <= index < len(self.scheduled_messages):
            self.scheduled_messages[index]['sent'] = True

    def remove_sent_messages(self):
        self.scheduled_messages = [msg for msg in self.scheduled_messages if not msg.get('sent', False)]