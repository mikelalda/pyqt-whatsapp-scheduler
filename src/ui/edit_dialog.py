from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QPushButton
from PyQt5.QtCore import QDateTime

class EditDialog(QDialog):
    def __init__(self, phone, message, time, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Scheduled Message")
        self.setMinimumWidth(300)
        layout = QVBoxLayout(self)

        self.phone_label = QLabel("Phone Number:")
        layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit(phone)
        layout.addWidget(self.phone_input)

        self.message_label = QLabel("Message:")
        layout.addWidget(self.message_label)
        self.message_input = QLineEdit(message)
        layout.addWidget(self.message_input)

        self.time_label = QLabel("Scheduled Time:")
        layout.addWidget(self.time_label)
        self.time_input = QDateTimeEdit()
        self.time_input.setDateTime(QDateTime.fromString(time))
        layout.addWidget(self.time_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def get_values(self):
        return (
            self.phone_input.text(),
            self.message_input.text(),
            self.time_input.dateTime().toString()
        )