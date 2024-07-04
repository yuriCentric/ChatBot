from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QTimer, QPropertyAnimation, QRect, QSequentialAnimationGroup, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QTextBlockFormat, QPixmap, QMovie
import sys
import getpass
import os
import psutil
import pyttsx3
from datetime import datetime, time
from chat_bot import process_input  # Assuming you have a chat_bot module with a process_input function

def get_first_name(username):
    return username.split('.')[0].capitalize()

class MovingLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("color: blue; font-size: 14px; font-weight: bold; font-family: Arial; padding: 0px")
        self.setAlignment(Qt.AlignCenter)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(25000)  # Slowed down the animation
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
        self.setStyleSheet("background-color: white;")

        self.move_to_bottom_right()
        self.layout = QVBoxLayout()
        
        self.moving_label = MovingLabel("This chatbot is designed for Centric India employees as a personal buddy.")
        self.layout.addWidget(self.moving_label)

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
                margin-top: 0px;  /* Reduce the margin to decrease top padding */
                margin-bottom: 0px;  /* Reduce the margin to decrease bottom padding */
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

        # Separator line
        self.separator = QLabel(self)
        self.separator.setFixedHeight(2)
        self.separator.setStyleSheet("background-color: #d3d3d3; margin: 5px 0;")
        self.layout.addWidget(self.separator)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(10, 10, 10, 10)

        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("Type your questions here ...")
        self.input_box.setStyleSheet("""
            QTextEdit {
                color: black;
                background-color: white;
                border-radius: 5px;
                font-family: Arial;
                font-size: 18px;
                padding: 10px;
                max-height: 60px; /* Limit height to 3 lines */
            }
        """)
        self.input_box.setFixedHeight(55)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.input_box.installEventFilter(self)

        self.send_button = QPushButton('', self)
        send_icon = QIcon(os.path.join('app', 'icons', 'send.png'))  # Ensure you have an appropriate send icon
        self.send_button.setIcon(send_icon)
        self.send_button.setIconSize(QSize(45, 45))  # Make send icon larger/smaller
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                margin-left: 11px;
                margin-bottom: 8px;
            }
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)

        self.input_layout.addWidget(self.input_box)
        self.input_layout.addWidget(self.send_button, alignment=Qt.AlignBottom)

        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)

        self.init_battery_check()
        self.init_reminder_popup()  # Initialize reminder popup

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 50, screen_geometry.height() - self.height() - 80)

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            self.new_chat_image.hide()  # Hide the new chat image when the first message is sent
            timestamp = datetime.now().strftime('%I:%M %p')
            self.append_message(user_input, timestamp, align_right=True)
            response = process_input(user_input)
            self.append_message(response, timestamp, align_right=False)
            self.input_box.clear()

    def append_message(self, message, timestamp, align_right=False):
        try:
            # Parse the provided timestamp and convert it to 12-hour format with AM/PM
            time_part = datetime.strptime(timestamp, '%I:%M %p').strftime('%I:%M %p')
            date_part = datetime.now().strftime('%A')  # Get current day of the week
            full_timestamp = f"{time_part}, {date_part}"
        except ValueError:
            # If the format is unexpected, use the timestamp as-is
            full_timestamp = timestamp

        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignRight if align_right else Qt.AlignLeft)
        cursor.insertBlock(block_format)

        user_style = """
            <div style="display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 10px;">
                <div style="background-color: #E8EAF6; color: black; padding: 10px 15px; border-radius: 15px; max-width: 75%; word-wrap: break-word;">
                    {message}
                    <div style="font-size: 14px; color: gray; text-align: right; margin-top: 5px;">{timestamp}</div>
                </div>
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

        self.new_chat_image.show()  # Show the new chat image when the chat is cleared

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
            elif battery.percent <= 20 and not battery.power_plugged:
                self.voice_alert("Battery is low. Please plug in the charger.")

    def voice_alert(self, message):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Set a slower speaking rate
        engine.say(message)
        engine.runAndWait()

    def init_reminder_popup(self):
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminder_time)
        self.reminder_timer.start(60000)  # Check every minute

    def check_reminder_time(self):
        now = datetime.now()
        if now.weekday() == 2:  # Check if today is Wednesday (0=Monday, 1=Tuesday, ..., 6=Sunday)
            reminder_times = [time(3, 30), time(9, 0), time(10, 0), time(11, 0), time(12, 0)]
            for reminder_time in reminder_times:
                if now.time().replace(second=0, microsecond=0) == reminder_time:
                    self.show_reminder_popup()

    def show_reminder_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Timesheet Reminder")
        msg.setText("A Reminder to fill timesheet today!")
        msg.setStandardButtons(QMessageBox.Close)
        msg.buttonClicked.connect(msg.close)
        
        # Show popup
        msg.show()
        
        # Play voice alert
        self.voice_alert("A Reminder to fill timesheet today!")

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)  # Make the window borderless and frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottom_layout = QHBoxLayout()
        self.layout.addLayout(self.bottom_layout)

        self.gif_label = QLabel(self)  # Change here from ClickableLabel to QLabel
        self.gif_label.setStyleSheet("background: transparent;")
        self.gif = QMovie(os.path.join('app', 'icons', 'your_gif.gif'))
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.gif_label.mousePressEvent = self.open_chat_window  # Connect mousePressEvent directly
        self.gif_label.setCursor(Qt.PointingHandCursor)  # Set cursor to pointing hand

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        self.move(screen_geometry.width() - self.width() + 300, screen_geometry.height() - self.height() + 200)

    def open_chat_window(self, event):
        self.chat_window = ChatbotApp()
        self.chat_window.show()
        self.chat_window.moving_label.start_animation()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: white;
        }
        QLineEdit {
            font-family: Arial;
            font-size: 18px;
            color: black;
            background-color: transparent;
            border: none;
            padding: 15px;
        }
        QLineEdit:focus {
            border: none;
            background-color: transparent;
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
            background-color: transparent;
            border: none;
            padding: 0px;
        }
        QTextEdit {
            font-family: Arial;
            font-size: 18px;
            color: black;
            background-color: white;
            border: none;
            padding: 2px 10px 10px 10px;
        }
        QLabel {
            color: lightgrey;
            font-family: Arial;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 5px;
        }
    """)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
