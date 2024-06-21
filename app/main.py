import sys
import getpass
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QMovie
from PyQt5.QtCore import Qt, pyqtSignal

from chat_bot import process_input  # Assuming you have a chat_bot module with a process_input function

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()

        # Get the system username
        username = getpass.getuser()

        # Set up the user interface
        self.setWindowTitle(f'Welcome to Centric, {username}')
        self.setGeometry(100, 100, 500, 600)
        self.setWindowIcon(QIcon('chat_icon.png'))  # Set an icon for the window (ensure you have an icon named chat_icon.png)
        self.layout = QVBoxLayout()
        self.title = QLabel('Your Centric ChatBot')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet("color: #fdb825; margin-bottom: 20px;")
        self.layout.addWidget(self.title)
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            color: #fdb825; 
            background-color: #2c1a5d;
            border: 1px solid #fdb825;
            padding: 5px;
            border-radius: 5px;
            font-family: Arial;
            font-size: 14px;
        """)
        self.layout.addWidget(self.chat_display)

        # Input box and buttons layout
        self.input_layout = QHBoxLayout()
        
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("""
            color: #2c1a5d; 
            background-color: white;
            border: 1px solid #fdb825;
            padding: 15px;
            border-radius: 15px;
            font-family: Arial;
            font-size: 14px;
        """)
        self.input_box.returnPressed.connect(self.send_message)  # Connect the return key press event to the send_message method
        self.input_layout.addWidget(self.input_box)

        # Button layout
        self.button_layout = QVBoxLayout()
        
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setIcon(QIcon('send_icon.png'))  # Ensure you have an icon named send_icon.png
        self.send_button.setStyleSheet("""
            background-color: #fdb825; 
            color: #2c1a5d; 
            font-size: 14px; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 15px;
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.button_layout.addWidget(self.send_button)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_chat)
        self.clear_button.setIcon(QIcon('clear_icon.png'))  # Ensure you have an icon named clear_icon.png
        self.clear_button.setStyleSheet("""
            background-color: #fdb825; 
            color: #2c1a5d; 
            font-size: 14px; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 15px;
        """)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.button_layout.addWidget(self.clear_button)

        self.input_layout.addLayout(self.button_layout)
        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)

    def send_message(self):
        user_input = self.input_box.text()
        if user_input:
            self.chat_display.append(f"You: {user_input}")
            response = process_input(user_input)
            self.chat_display.append(f"Chatbot: {response}")
            self.input_box.clear()

    def clear_chat(self):
        self.chat_display.clear()

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.setWindowTitle('Welcome to Centric')
        self.setWindowFlag(Qt.FramelessWindowHint)  # Make the window borderless and frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.setWindowIcon(QIcon('chat_icon.png'))  # Set an icon for the window (ensure you have an icon named chat_icon.png)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create a horizontal layout to hold the GIF and spacer
        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        # Add the GIF label
        self.gif_label = ClickableLabel(self)
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(r'C:/Users/sagar.patel/OneDrive - Centric Consulting/Documents/GitHub/ChatBot/icons/your_gif.gif')  # Ensure you have a GIF named your_gif.gif
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Add a spacer to push the GIF to the left
        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.gif_label.clicked.connect(self.open_chat_window)

        # Add a spacer to push everything up
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def open_chat_window(self):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #1e1e2e;
        }
        QLineEdit {
            font-family: Arial;
            font-size: 14px;
            color: #2c1a5d;
            background-color: white;
            border: 1px solid #fdb825;
            padding: 15px;
            border-radius: 15px;
        }
        QPushButton {
            background-color: #fdb825;
            color: #2c1a5d;
            font-size: 14px;
            border: none;
            padding: 10px 20px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #e0a513;
        }
        QTextEdit {
            font-family: Arial;
            font-size: 14px;
            color: #fdb825;
            background-color: #2c1a5d;
            border: 1px solid #fdb825;
            padding: 15px;
            border-radius: 15px;
        }
        QLabel {
            color: #fdb825;
            font-family: Arial;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        QScrollBar:vertical {
            border: none;
            background-color: #2c1a5d;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #fdb825;
            min-height: 25px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
