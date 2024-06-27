import sys
import getpass
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QFont, QIcon, QMovie, QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
import os

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
        self.resize(500, 600)
        self.setWindowIcon(QIcon(os.path.join('icons', 'your_gif.gif')))  # Set an icon for the window

        # Position the window at the bottom right corner
        self.move_to_bottom_right()
        self.layout = QVBoxLayout()
        self.title = QLabel('Your Centric Buddy')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet("color: #2c1a5d; margin-bottom: 20px;")
        self.layout.addWidget(self.title)
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            color: black; 
            background-color: white;
            border: 1px solid #2c1a5d;
            padding: 5px;
            border-radius: 5px;
            font-family: Arial;
            font-size: 14px;
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                min-height: 25px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
                color: #333;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.layout.addWidget(self.chat_display)

        # Input box and buttons layout
        self.input_layout = QHBoxLayout()
        
        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("""
            color: black; 
            background-color: white;
            border: 1px solid #2c1a5d;
            padding: 10px;
            border-radius: 15px;
            font-family: Arial;
            font-size: 14px;
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                min-height: 25px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
                color: #333;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.input_box.setFixedHeight(80)  # Fixed height to maintain size
        self.input_box.installEventFilter(self)
        self.input_layout.addWidget(self.input_box)

        # Button layout
        self.button_layout = QVBoxLayout()
        
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            background-color: #2c1a5d; 
            color: white; 
            font-size: 14px; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 15px;
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.button_layout.addWidget(self.send_button)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_chat)
        self.clear_button.setStyleSheet("""
            background-color: #2c1a5d; 
            color: white; 
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

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            self.append_message(f"You: {user_input}", align_right=True)
            response = process_input(user_input)
            self.append_message(f"Chatbot: {response}", align_right=False)
            self.input_box.clear()

    def append_message(self, message, align_right=False):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignRight if align_right else Qt.AlignLeft)
        cursor.insertBlock(block_format)
        cursor.insertText(message)
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def clear_chat(self):
        self.chat_display.clear()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and source is self.input_box):
            if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
                self.send_message()
                return True
            elif event.key() == Qt.Key_Return and (event.modifiers() & Qt.ShiftModifier):
                # Allow shift+enter to insert new line
                self.input_box.insertPlainText("\n")
                return True
        return super(ChatbotApp, self).eventFilter(source, event)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.setWindowTitle('Welcome to Centric')
        self.setWindowFlag(Qt.FramelessWindowHint)  # Make the window borderless and frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create a horizontal layout to hold the GIF and spacer
        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        # Add the GIF label
        self.gif_label = ClickableLabel(self)
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(os.path.join('icons', 'your_gif.gif'))  # Ensure you have a GIF named your_gif.gif
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        # Add a spacer to push the GIF to the left
        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.gif_label.clicked.connect(self.open_chat_window)

        # Add a spacer to push everything up
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Position the window at the bottom right corner
        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

    def open_chat_window(self):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #eaeaea;
        }
        QLineEdit, QTextEdit {
            font-family: Arial;
            font-size: 14px;
            color: black;
            background-color: white;
            border: 1px solid #2c1a5d;
            padding: 15px;
            border-radius: 15px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #2c1a5d;
            background-color: white;
        }
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 8px;  /* Thinner scroll bar */
        }
        QScrollBar::handle:vertical {
            background-color: #a0a0a0;  /* Darker grey for the handle */
            min-height: 25px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
            color: #333;  /* Dark grey arrows */
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        QPushButton {
            background-color: #2c1a5d;
            color: white;
            font-size: 14px;
            border: none;
            padding: 10px 20px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #24174d;
        }
        QTextEdit {
            font-family: Arial;
            font-size: 14px;
            color: black;
            background-color: white;
            border: 1px solid #2c1a5d;
            padding: 15px;
            border-radius: 15px;
        }
        QLabel {
            color: #2c1a5d;
            font-family: Arial;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    """)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
