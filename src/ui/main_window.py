from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateTimeEdit, QMessageBox, QListWidget, QHBoxLayout, QTextEdit, QFileDialog
)
from PyQt5.QtCore import QDateTime, QTimer
import pywhatkit
from datetime import datetime
from scheduler.message_scheduler import MessageScheduler
from ui.edit_dialog import EditDialog
import pyautogui
import time
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WhatsApp Message Scheduler")
        self.setGeometry(100, 100, 450, 600)

        self.scheduler = MessageScheduler()
        self.selected_index = None
        self.file_path = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.phone_label = QLabel("Phone Number (with country code):")
        self.layout.addWidget(self.phone_label)

        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_input)

        self.message_label = QLabel("Message:")
        self.layout.addWidget(self.message_label)

        self.message_input = QTextEdit()
        self.layout.addWidget(self.message_input)

        self.file_layout = QHBoxLayout()
        self.select_file_button = QPushButton("Select Image")
        self.select_file_button.clicked.connect(self.select_file)
        self.file_layout.addWidget(self.select_file_button)

        self.clear_file_button = QPushButton("Clear Image")
        self.clear_file_button.clicked.connect(self.clear_file)
        self.file_layout.addWidget(self.clear_file_button)
        self.layout.addLayout(self.file_layout)

        self.file_path_label = QLabel("No image selected.")
        self.layout.addWidget(self.file_path_label)

        self.schedule_label = QLabel("Schedule Time:")
        self.layout.addWidget(self.schedule_label)

        self.schedule_input = QDateTimeEdit()
        self.schedule_input.setDateTime(QDateTime.currentDateTime())
        self.layout.addWidget(self.schedule_input)

        self.button_layout = QHBoxLayout()
        self.schedule_button = QPushButton("Schedule Message")
        self.schedule_button.clicked.connect(self.schedule_message)
        self.button_layout.addWidget(self.schedule_button)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_selected_message)
        self.button_layout.addWidget(self.edit_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_message)
        self.button_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.button_layout)

        self.scheduled_list = QListWidget()
        self.scheduled_list.clicked.connect(self.on_message_selected)
        self.layout.addWidget(self.scheduled_list)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_send_messages)
        self.timer.start(10000)  # check every 10 seconds

        self.refresh_scheduled_list()


    def select_file(self):
        # Filtramos para que solo se puedan seleccionar imágenes
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image to Send", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.file_path = file_name
            self.file_path_label.setText(f"Image: {os.path.basename(file_name)}")

    def clear_file(self):
        self.file_path = None
        self.file_path_label.setText("No image selected.")

    def schedule_message(self):
        phone = self.phone_input.text()
        message = self.message_input.toPlainText()
        schedule_time = self.schedule_input.dateTime()

        if not phone or (not message and not self.file_path):
            QMessageBox.warning(self, "Input Error", "Please provide a phone number and either a message or an image.")
            return

        # Pasa el file_path al scheduler
        self.scheduler.schedule_message(phone, message, schedule_time.toString(), self.file_path)
        self.refresh_scheduled_list()
        self.clear_file()
        QMessageBox.information(self, "Message Scheduled", f"Message scheduled for {schedule_time.toString()}")

    def refresh_scheduled_list(self):
        self.scheduled_list.clear()
        for msg in self.scheduler.get_scheduled_messages():
            status = "SENT" if msg.get('sent', False) else "PENDING"
            file_info = ""
            if msg.get('file_path'):
                file_info = f" [Image: {os.path.basename(msg['file_path'])}]"
            self.scheduled_list.addItem(f"{msg['user']} -- {msg['message'].replace(chr(10), ' ')}{file_info} -- at {msg['time']} [{status}]")
            
    def on_message_selected(self):
        self.selected_index = self.scheduled_list.currentRow()
        if self.selected_index is not None and self.selected_index >= 0:
            msg = self.scheduler.get_scheduled_messages()[self.selected_index]
            self.phone_input.setText(msg['user'])
            self.message_input.setText(msg['message'])
            dt = QDateTime.fromString(msg['time'])
            if dt.isValid():
                self.schedule_input.setDateTime(dt)
            if msg.get('file_path'):
                self.file_path = msg.get('file_path')
                self.file_path_label.setText(f"Image: {os.path.basename(self.file_path)}")
            else:
                self.clear_file()

    def remove_selected_message(self):
        if self.selected_index is not None and self.selected_index >= 0:
            self.scheduler.remove_message(self.selected_index)
            self.refresh_scheduled_list()
            self.selected_index = None
            self.phone_input.clear()
            self.message_input.clear()
            self.schedule_input.setDateTime(QDateTime.currentDateTime())
            self.clear_file()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a message to remove.")
            
    def edit_selected_message(self):
        if self.selected_index is not None and self.selected_index >= 0:
            msg = self.scheduler.get_scheduled_messages()[self.selected_index]
            dialog = EditDialog(msg['user'], msg['message'], msg['time'], msg['file_path'], self)
            if dialog.exec_():
                phone, message, schedule_time = dialog.get_values()
                self.scheduler.edit_message(self.selected_index, phone, message, schedule_time)
                self.refresh_scheduled_list()
                QMessageBox.information(self, "Message Edited", "Scheduled message updated.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a message to edit.")

    def check_and_send_messages(self):
        now = QDateTime.currentDateTime()
        messages_to_process = self.scheduler.get_scheduled_messages()
        
        for idx, msg in enumerate(messages_to_process):
            if not msg.get('sent', False):
                scheduled_time = QDateTime.fromString(msg['time'])
                
                if scheduled_time <= now:
                    try:
                        file_path = msg.get('file_path')
                        
                        # Si hay una ruta de archivo, usamos la función con pyautogui
                        if file_path:
                            pywhatkit.sendwhats_image(
                                msg['user'],
                                file_path,
                                msg['message'],
                                wait_time=15,
                                tab_close=True
                            )
                        # Si no hay archivo, usamos la lógica original para texto
                        else:
                            pywhatkit.sendwhatmsg_instantly(
                                msg['user'],
                                msg['message'],
                                wait_time=15,
                                tab_close=True
                            )
                        # Espera un poco para que el mensaje se escriba
                        time.sleep(5)
                        # Pulsa Enter para enviar el mensaje
                        print("Pressing Enter to send the message...")
                        pyautogui.press('enter')

                        self.scheduler.mark_as_sent(idx)
                    except Exception as e:
                        QMessageBox.warning(self, "Send Error", f"Failed to send message: {e}")
        
        self.scheduler.remove_sent_messages()
        self.refresh_scheduled_list()