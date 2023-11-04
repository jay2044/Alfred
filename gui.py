import sys
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import json
from PyQt5.QtCore import *
# from vosk import Model, KaldiRecognizer
import os
# import pyaudio
import pyttsx3
import threading
from stt import STT
import winsound


class SendMessageThread(QThread):
    finished = pyqtSignal(list)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        response = requests.post('http://localhost:5005/webhooks/rest/webhook',
                                 json={"message": self.message})
        self.finished.emit(response.json())


class ChatApplication(QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()
        # Check if Rasa server is already running
        try:
            requests.get('http://localhost:5005/status')
            print("Rasa server already running.")
        except requests.exceptions.ConnectionError:
            # If not, start Rasa server
            self.rasa_server = subprocess.Popen(['rasa', 'run', '--enable-api'])
        try:
            requests.get("http://localhost:5055")
            print("Rasa action server already running.")
        except requests.exceptions.ConnectionError:
            # Start Rasa action server
            self.rasa_action_server = subprocess.Popen(['rasa', 'run', 'actions'])
        # Set status to loading
        self.status_label.setText('Loading...')

        # Start timer to periodically check server status
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_server_status)
        self.timer.start(5000)  # Check every 5 seconds

        # TTS engine
        self.engine = pyttsx3.init()

        # Add shortcut for Enter key
        self.shortcut = QShortcut(QKeySequence("Return"), self)
        self.shortcut.activated.connect(self.send_message)

    def check_server_status(self):
        response = self.send_to_rasa("test")
        if response is not None:
            self.status_label.setText('Ready')
            self.timer.stop()
            self.stt = STT()
            self.stt.user_spoke.connect(self.handle_user_speech)
            self.toggle_mic(True)

    def send_to_rasa(self, message):
        try:
            response = requests.post('http://localhost:5005/webhooks/rest/webhook',
                                     json={"message": message}, timeout=5)
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def init_ui(self):
        self.setWindowTitle('Chatbot')
        # Vertical layout
        self.layout = QVBoxLayout()
        # Add widgets to layout
        self.button = QPushButton('Send')
        self.mic_button = QPushButton('Mic Off')
        self.mic_button.setCheckable(True)
        self.mic_button.setChecked(True)
        self.mic_button.toggled.connect(self.toggle_mic)
        self.chatbox = QTextEdit()
        self.text_input = QLineEdit()
        self.status_label = QLabel()
        # Set chatbox to readonly
        self.chatbox.setReadOnly(True)
        # Connect button to send_message function
        self.button.clicked.connect(self.send_message)
        # Add widgets to layout
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.chatbox)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.mic_button)
        # Set window layout
        self.setLayout(self.layout)

    def send_message(self):
        message = self.text_input.text().strip()  # Remove leading/trailing white spaces
        self.text_input.clear()
        if message:  # Check if message is not an empty string
            # Send user message to Rasa server
            self.thread = SendMessageThread(message)
            self.chatbox.append("User: " + message)
            self.thread.finished.connect(self.handle_server_response)
            self.thread.start()

    def handle_server_response(self, response):
        # Get bot responses from Rasa server
        bot_responses = [message['text'] for message in response]
        # Display bot responses in chatbox
        for bot_response in bot_responses:
            self.chatbox.append("Bot: " + bot_response)
            self.TTS(bot_response)

    def handle_user_speech(self, text):
        text = text.strip()  # Remove leading/trailing white spaces
        if text:  # Check if text is not an empty string
            self.chatbox.append("User: " + text)
            # Send user message to Rasa server
            self.thread = SendMessageThread(text)
            self.thread.finished.connect(self.handle_server_response)
            self.thread.start()

    def closeEvent(self, event):
        # Initiate shutdown of the Rasa server and Rasa action server
        self.rasa_server.terminate()
        self.rasa_action_server.terminate()
        # Wait for the processes to finish
        self.rasa_server.wait()
        self.rasa_action_server.wait()
        # Proceed with the remaining shutdown process
        event.accept()
        self.stt.keep_listening = False
        self.stt.stop()

    def toggle_mic(self, checked):
        if checked:
            # If the button was just clicked, start the Vosk listening process
            self.stt.keep_listening = True  # Set the flag to True
            self.audio_thread = threading.Thread(target=self.stt.run)
            self.mic_button.setText('Mic On')
            winsound.Beep(2500, 200)
            self.audio_thread.start()
        else:
            # If the button was just un-clicked, stop the Vosk listening process
            self.mic_button.setText('Mic Off')
            self.stt.keep_listening = False  # Set the flag to False

    def TTS(self, text):
        self.toggle_mic(False)
        self.engine.say(text)
        QCoreApplication.processEvents()  # to update GUI immediately
        self.engine.runAndWait()
        self.toggle_mic(True)


app = QApplication(sys.argv)

chat_app = ChatApplication()
chat_app.show()

sys.exit(app.exec_())
