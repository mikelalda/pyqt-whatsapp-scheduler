# PyQt WhatsApp Scheduler

This project is a PyQt application that allows users to read messages and schedule message sending for WhatsApp contacts or groups. It provides a user-friendly interface for managing message scheduling and reading incoming messages.

## Features

- Schedule messages to be sent at specific times.
- Read incoming messages from WhatsApp.
- User-friendly interface built with PyQt.
- Input validation and formatting utilities.

## Project Structure

```
pyqt-whatsapp-scheduler
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui
│   │   └── main_window.py     # Defines the main window and user interface
│   ├── scheduler
│   │   └── message_scheduler.py # Manages message scheduling
│   ├── whatsapp
│   │   └── message_reader.py   # Reads incoming messages from WhatsApp
│   └── utils
│       └── helpers.py          # Utility functions for the application
├── requirements.txt            # Lists project dependencies
└── README.md                   # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pyqt-whatsapp-scheduler
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Use the interface to read messages and schedule new messages to be sent.

## Crear un ejecutable

Puedes crear un ejecutable de la aplicación usando PyInstaller.  
Sigue estos pasos:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Genera el ejecutable:
   ```
   pyinstaller --onefile --windowed src/main.py
   ```

   El ejecutable se generará en la carpeta `dist`.

3. Ejecuta el archivo generado:
   ```
   dist\main.exe
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.