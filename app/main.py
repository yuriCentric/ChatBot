import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QDesktopWidget
from PyQt5.QtCore import Qt, QEvent, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QTextBlockFormat, QPixmap, QMovie
import sys
import getpass
import os
from datetime import datetime
from chatterbot import ChatBot
from config import MONGO_URI
from alerts import BatteryAlert, check_reminder_time, show_reminder_popup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

chatbot = ChatBot('CI-Buddy', storage_adapter='chatterbot.storage.MongoDatabaseAdapter', database_uri=MONGO_URI)

def process_input(message):
    response = chatbot.get_response(message)
    return response.text

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()

        username = getpass.getuser()
        self.user_first_name = username.split('.')[0].capitalize()

        self.setWindowTitle(f'Welcome, {self.user_first_name}')
        self.resize(500, 600)
        self.setWindowIcon(QIcon(os.path.join('app', 'icons', 'your_png.png')))
        self.setStyleSheet(open('app/css/main.css').read())

        self.move_to_bottom_right()
        self.layout = QVBoxLayout()

        self.title = QLabel('Hi, I am your Centric Buddy')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 20, QFont.Bold))
        self.title.setStyleSheet("color: #A6A6A6; background-color: #f2f2f2; padding: 20px; border-radius: 10px;")
        self.layout.addWidget(self.title)

        self.new_chat_image = QLabel(self)
        self.new_chat_image.setPixmap(QPixmap(os.path.join('app', 'icons', 'newchat.png')))
        self.new_chat_image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.new_chat_image)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: black;
                background-color: white;
                border-radius: 5px;
                padding: 5px;
                font-family: Arial;
                font-size: 18px;
                margin-top: 0px;
                margin-bottom: 0px;
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

        self.separator = QLabel(self)
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet("background-color: #d3d3d3; margin: 5px 0;")
        self.layout.addWidget(self.separator)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(5, 5, 5, 5)

        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("Type your query here ...")
        self.input_box.setStyleSheet("""
            QTextEdit {
                color: black;
                background-color: white;
                border-radius: 5px;
                font-family: Arial;
                font-size: 18px;
                padding: 5px;
                max-height: 55px;
            }
        """)
        self.input_box.setFixedHeight(55)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.input_box.installEventFilter(self)

        self.send_button = QPushButton('', self)
        send_icon = QIcon(os.path.join('app', 'icons', 'send.png'))
        self.send_button.setIcon(send_icon)
        self.send_button.setIconSize(QSize(35, 35))
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                margin-left: 5px;
                margin-bottom: 12px;
            }
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)

        self.input_layout.addWidget(self.input_box)
        self.input_layout.addWidget(self.send_button, alignment=Qt.AlignBottom)

        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)

        self.init_battery_check()
        self.init_reminder_popup()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 5, screen_geometry.height() - self.height() - 50)

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            self.new_chat_image.hide()
            timestamp = datetime.now().strftime('%I:%M %p')
            self.append_message(user_input, timestamp, align_right=True)
            response = process_input(user_input)
            self.append_message(response, timestamp, align_right=False)
            self.input_box.clear()

    def append_message(self, message, timestamp, align_right=False):
        try:
            time_part = datetime.strptime(timestamp, '%I:%M %p').strftime('%I:%M %p')
            date_part = datetime.now().strftime('%A')
            full_timestamp = f"{time_part}, {date_part}"
        except ValueError:
            full_timestamp = timestamp

        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignRight if align_right else Qt.AlignLeft)
        cursor.insertBlock(block_format)

        user_style = """
                <div style="background-color: #E8E8E8; color: black; padding: 10px; border-radius: 5px; max-width: 75%; word-wrap: break-word;">
                    {message}
                    <div style="font-size: 14px; color: gray; text-align: right; margin-top: 5px;">{timestamp}</div>
                </div>
        """
        
        bot_style = """
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <img src='app/icons/chat.png' width='30' height='30' style="margin-right: 10px; border-radius: 50%;" />
                <div style="background-color: #1A73E8; color: white; padding: 10px 15px; border-radius: 25px; max-width: 75%; word-wrap: break-word; display: flex; flex-direction: column;">
                    <div>{message}</div>
                    <div style="font-size: 14px; color: gray; text-align: left; margin-top: 5px;">{timestamp}</div>
                </div>
            </div>
        """
        
        formatted_message = user_style.format(message=message, timestamp=full_timestamp) if align_right else bot_style.format(message=message, timestamp=full_timestamp)
        
        cursor.insertHtml(formatted_message)
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def clear_chat(self):
        self.chat_display.clear()
        self.new_chat_image.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.input_box:
            if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
                self.send_message()
                return True
            elif event.key() == Qt.Key_Return and (event.modifiers() & Qt.ShiftModifier):
                self.input_box.insertPlainText("\n")
                return True
        return super(ChatbotApp, self).eventFilter(source, event)

    def init_battery_check(self):
        self.battery_alert = BatteryAlert()

    def init_reminder_popup(self):
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminder_time)
        self.reminder_timer.start(60000)

    def check_reminder_time(self):
        reminder_message = check_reminder_time()
        if reminder_message:
            self.append_message(reminder_message, datetime.now().strftime('%I:%M %p'), align_right=False)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        self.gif_label = QLabel(self)
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(os.path.join('app', 'icons', 'your_gif.gif'))
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.gif_label.mousePressEvent = self.open_chat_window
        self.gif_label.setCursor(Qt.PointingHandCursor)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() + 300, screen_geometry.height() - self.height() + 150)

    def open_chat_window(self, event):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('app/css/main.css').read())
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())


    def clear_chat(self):
        self.chat_display.clear()
        self.new_chat_image.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.input_box:
            if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier):
                self.send_message()
                return True
            elif event.key() == Qt.Key_Return and (event.modifiers() & Qt.ShiftModifier):
                self.input_box.insertPlainText("\n")
                return True
        return super(ChatbotApp, self).eventFilter(source, event)

    def init_battery_check(self):
        self.battery_alert = BatteryAlert()

    def init_reminder_popup(self):
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminder_time)
        self.reminder_timer.start(60000)

    def check_reminder_time(self):
        reminder_message = check_reminder_time()
        if reminder_message:
            self.append_message(reminder_message, datetime.now().strftime('%I:%M %p'), align_right=False)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        self.gif_label = QLabel(self)
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(os.path.join('app', 'icons', 'your_gif.gif'))
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.gif_label.mousePressEvent = self.open_chat_window
        self.gif_label.setCursor(Qt.PointingHandCursor)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() + 300, screen_geometry.height() - self.height() + 150)

    def open_chat_window(self, event):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('app/css/main.css').read())
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
