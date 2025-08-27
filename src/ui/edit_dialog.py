from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QDateTimeEdit, QPushButton, QFileDialog, QTextEdit
)
from PyQt5.QtCore import QDateTime
import os

class EditDialog(QDialog):
    def __init__(self, phone, message, time, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Scheduled Message")
        self.setMinimumWidth(350)
        self.file_path = file_path
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

        self.file_label = QLabel("Attached Image:")
        layout.addWidget(self.file_label)
        
        self.file_path_label = QLabel()
        self.update_file_label()
        layout.addWidget(self.file_path_label)

        file_button_layout = QHBoxLayout()
        self.select_file_button = QPushButton("Select New Image")
        self.select_file_button.clicked.connect(self.select_file)
        file_button_layout.addWidget(self.select_file_button)

        self.clear_file_button = QPushButton("Clear Image")
        self.clear_file_button.clicked.connect(self.clear_file)
        file_button_layout.addWidget(self.clear_file_button)
        
        layout.addLayout(file_button_layout)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.file_path = file_name
            self.update_file_label()

    def clear_file(self):
        self.file_path = None
        self.update_file_label()
        
    def update_file_label(self):
        if self.file_path:
            self.file_path_label.setText(f"Current: {os.path.basename(self.file_path)}")
        else:
            self.file_path_label.setText("No image selected.")

    def get_values(self):
        return (
            self.phone_input.text(),
            self.message_input.text(), 
            self.time_input.dateTime().toString(),
            self.file_path 
        )