import sys
import getpass
import os
import psutil
import pyttsx3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QFont, QIcon, QMovie, QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QTimer, QPropertyAnimation, QRect, QSequentialAnimationGroup

from chat_bot import process_input  # Assuming you have a chat_bot module with a process_input function

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()

def get_first_name(username):
    return username.split('.')[0].capitalize()

class MovingLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("color: red; font-size: 14px; font-weight: bold; font-family: Arial;")
        self.setAlignment(Qt.AlignCenter)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(30000)  # Slowed down the animation
        screen_width = QApplication.desktop().screenGeometry().width()
        self.animation.setStartValue(QRect(screen_width, 0, screen_width, 50))  # Start off screen on the right
        self.animation.setEndValue(QRect(-screen_width, 0, screen_width, 50))  # End off screen on the left
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.setLoopCount(-1)  # Infinite loop

    def start_animation(self):
        self.animation_group.start()

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()

        username = getpass.getuser()
        self.user_first_name = get_first_name(username)

        self.setWindowTitle(f'Welcome, {self.user_first_name}')
        self.resize(500, 600)
        self.setWindowIcon(QIcon(os.path.join('app', 'icons', 'your_png.png')))

        self.move_to_bottom_right()
        self.layout = QVBoxLayout()

        self.moving_label = MovingLabel("This chatbot is designed for Centric India employees as a personal buddy.")
        self.layout.addWidget(self.moving_label)

        self.title = QLabel('Hi, I am your Centric Buddy')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 26, QFont.Bold))
        self.title.setStyleSheet("color: #2c1a5d; margin-top: 0px; margin-bottom: 5px;")
        self.layout.addWidget(self.title)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: black; 
                background-color: white;
                border: 1px solid #2c1a5d;
                padding: 5px;
                border-radius: 5px;
                font-family: Arial;
                font-size: 18px;
            }
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

        self.input_layout = QHBoxLayout()
        
        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("""
            QTextEdit {
                color: black; 
                background-color: white;
                border: 1px solid #2c1a5d;
                padding: 10px;
                border-radius: 15px;
                font-family: Arial;
                font-size: 18px;
            }
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
                background: none.
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none.
                color: #333.
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none.
            }
        """)
        self.input_box.setFixedHeight(95)  # Fixed height to maintain size
        self.input_box.installEventFilter(self)
        self.input_layout.addWidget(self.input_box)

        self.button_layout = QVBoxLayout()
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2c1a5d; 
                color: white; 
                font-size: 18px; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #24174d;
            }
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.button_layout.addWidget(self.send_button)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_chat)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #2c1a5d; 
                color: white; 
                font-size: 18px; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #24174d;
            }
        """)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.button_layout.addWidget(self.clear_button)
        self.input_layout.addLayout(self.button_layout)
        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)

        self.init_battery_check()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            timestamp = datetime.now().strftime('%H:%M')
            self.append_message(f"<span style='font-size:12px;'>{timestamp}</span>\n", align_right=True)
            self.append_message(f"{user_input} <b>:You</b>", align_right=True)
            response = process_input(user_input)
            timestamp = datetime.now().strftime('%H:%M')
            self.append_message(f"<span style='font-size:12px;'>{timestamp}</span>\n", align_right=False)

            # Format the entire response text with a background color
            formatted_response = f"<b>CI-Buddy:</b> <span style='background-color: #e6ffe6; padding: 5px; border-radius: 10px; display: inline-block;'>{response}</span>"
            
            self.append_message(formatted_response, align_right=False)
            
            self.input_box.clear()

    def append_message(self, message, align_right=False):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignRight if align_right else Qt.AlignLeft)
        cursor.insertBlock(block_format)
        
        if align_right:
            # User message bubble color with spacing
            formatted_message = f"<div style='background-color: #d2e8ff; padding: 5px; border-radius: 10px; margin-bottom: 10px; max-width: 75%;'>{message}</div>"
        else:
            # Bot message bubble color with spacing
            formatted_message = f"<div style='background-color: #f0f0f0; padding: 5px; border-radius: 10px; margin-bottom: 10px; max-width: 75%;'>{message}</div>"
        
        cursor.insertHtml(formatted_message)
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
                self.input_box.insertPlainText("\n")
                return True
        return super(ChatbotApp, self).eventFilter(source, event)

    def init_battery_check(self):
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.check_battery)
        self.battery_timer.start(60000)  # Check every minute

    def check_battery(self):
        battery = psutil.sensors_battery()
        if battery is not None:
            if battery.percent >= 95 and battery.power_plugged:
                self.voice_alert("Battery is full. Please unplug the charger.")
                self.voice_alert("Battery is full. Please unplug the charger.")
            elif battery.percent <= 20 and not battery.power_plugged:
                self.voice_alert("Battery is low. Please plug in the charger.")
                self.voice_alert("Battery is low. Please plug in the charger.")

    def voice_alert(self, message):
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)  # Make the window borderless and frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        self.gif_label = ClickableLabel(self)
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(os.path.join('app', 'icons', 'your_gif.gif'))
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.gif_label.clicked.connect(self.open_chat_window)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

    def open_chat_window(self):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.chat_window.moving_label.start_animation()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #eaeaea;
        }
        QLineEdit, QTextEdit {
            font-family: Arial;
            font-size: 18px;
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
            width: 8px;
        }
        QScrollBar::handle:vertical {
            background-color: #a0a0a0;
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
        QPushButton {
            background-color: #2c1a5d;
            color: white;
            font-size: 18px;
            border: none;
            padding: 10px 20px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #24174d;
        }
        QTextEdit {
            font-family: Arial;
            font-size: 18px;
            color: black;
            background-color: white;
            border: 1px solid #2c1a5d;
            padding: 15px;
            border-radius: 15px;
        }
        QLabel {
            color: #2c1a5d;
            font-family: Arial;
            font-size: 25px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    """)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
