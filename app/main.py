import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QDesktopWidget, QDialog, QScrollArea
from PyQt5.QtCore import Qt, QEvent, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QTextBlockFormat, QPixmap, QMovie, QImage
import sys
import getpass
import os
from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from alerts import BatteryAlert, check_reminder_time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import webbrowser
import fitz  # PyMuPDF
from celebrations import get_today_birthdays, get_today_anniversaries, get_email_by_name  # Import the celebration logic

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def find_best_match(user_input):
    # Fetch all documents from the collection
    documents = list(collection.find())
    if not documents:
        print('No documents found in the collection.')
        return 'Sorry, I could not find a suitable answer.'

    if user_input.startswith("send birthday wishes to "):
        name = user_input[len("send birthday wishes to "):].strip()
        excel_path = os.path.join('app', 'sqa.xlsx')
        email = get_email_by_name(excel_path, name)
        if email:
            subject = "Happy Birthday!!"
            body = (
                        "Wishing you a very Happy Birthday!\n\n"
                        "\n\n May your special day be filled with joy, laughter, and wonderful moments. "
                    )

            return draft_email(email, subject, body)
        else:
            return f"Could not find email for {name}."

    if user_input.startswith("send anniversary wishes to "):
        name = user_input[len("send anniversary wishes to "):].strip()
        excel_path = os.path.join('app', 'sqa.xlsx')
        email = get_email_by_name(excel_path, name)
        if email:
            subject = "Happy Anniversary!!"
            body = "Congratulations on your Work Anniversary!"
            return draft_email(email, subject, body)
        else:
            return f"Could not find email for {name}."

    inputs = [doc.get('input', '') for doc in documents]
    responses = [doc.get('response', '') for doc in documents]

    # Filter out non-string inputs
    non_empty_inputs = [(input_text.strip(), response) for input_text, response in zip(inputs, responses) if isinstance(input_text, str) and input_text.strip()]

    if not non_empty_inputs:
        print('All inputs are empty or invalid.')
        return 'Sorry, I am unable to understand and could not find a suitable answer for you. Try reframing your question. '

    inputs, responses = zip(*non_empty_inputs)

    # Include the user_input in the list of documents for TF-IDF vectorization
    all_texts = list(inputs) + [user_input]

    # Vectorize the texts
    vectorizer = TfidfVectorizer().fit_transform(all_texts)
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the user input and all stored inputs
    cosine_similarities = cosine_similarity([vectors[-1]], vectors[:-1]).flatten()

    # Find the index of the best match
    best_match_index = np.argmax(cosine_similarities)
    highest_similarity = cosine_similarities[best_match_index]

    # Debug: Print similarity scores
    print('User input:', user_input)
    print('Inputs:', inputs)
    print('Responses:', responses)
    print('TF-IDF Vectors:', vectors)
    print('Cosine Similarities:', cosine_similarities)
    print('Best match index:', best_match_index)
    print('Highest similarity:', highest_similarity)
    print('Best match input:', inputs[best_match_index])
    print('Best match response:', responses[best_match_index])

    # Threshold for considering a match suitable
    threshold = 0.4

    if highest_similarity > threshold:
        return responses[best_match_index]
    else:
        return 'Sorry, I am unable to understand and could not find a suitable answer for you. Try reframing your question.'

def draft_email(recipient_email, subject, body):
    mailto_link = f"mailto:{recipient_email}?subject={subject}&body={body}"
    try:
        webbrowser.open(mailto_link)
        return "Email draft triggered successfully."
    except Exception as e:
        return f"Failed to trigger email draft: {str(e)}"

class ReadmeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Readme")
        self.resize(600, 800)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.load_pdf(os.path.join('app', 'readme.pdf'))

    def load_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                qt_image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

                label = QLabel(self.scroll_content)
                label.setPixmap(QPixmap.fromImage(qt_image))
                self.scroll_layout.addWidget(label)

            self.scroll_layout.addStretch()
        except Exception as e:
            print(f"Error loading PDF: {e}")

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()

        # Add a new attribute to store UMX details
        self.umx_details = {}
        self.umx_form = None
        
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

        # Add icons for Centric logo, birthday, anniversary, clear chat, and help
        self.icons_layout = QHBoxLayout()

        self.logo_icon = QLabel(self)
        self.logo_icon.setPixmap(QPixmap(os.path.join('app', 'icons', 'logo.png')).scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icons_layout.addWidget(self.logo_icon)

        self.icons_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.cake_icon = QLabel(self)
        self.cake_icon.setPixmap(QPixmap(os.path.join('app', 'icons', 'bday.png')).scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.cake_icon.setToolTip(self.get_birthday_tooltip())
        self.icons_layout.addWidget(self.cake_icon)

        self.anniversary_icon = QLabel(self)
        self.anniversary_icon.setPixmap(QPixmap(os.path.join('app', 'icons', 'anv.png')).scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.anniversary_icon.setToolTip(self.get_anniversary_tooltip())
        self.icons_layout.addWidget(self.anniversary_icon)

        self.clear_icon = QLabel(self)
        self.clear_icon.setPixmap(QPixmap(os.path.join('app', 'icons', 'clear.png')).scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.clear_icon.setCursor(Qt.PointingHandCursor)
        self.clear_icon.setToolTip('Clear Chat')
        self.clear_icon.mousePressEvent = self.clear_chat
        self.icons_layout.addWidget(self.clear_icon)

        self.help_icon = QLabel(self)
        self.help_icon.setPixmap(QPixmap(os.path.join('app', 'icons', 'help.png')).scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.help_icon.setCursor(Qt.PointingHandCursor)
        self.help_icon.setToolTip('Help')
        self.help_icon.mousePressEvent = self.open_readme
        self.icons_layout.addWidget(self.help_icon)

        self.layout.addLayout(self.icons_layout)
        self.layout.setAlignment(self.icons_layout, Qt.AlignTop)

        self.new_chat_image = QLabel(self)
        self.new_chat_image.setPixmap(QPixmap(os.path.join('app', 'icons', 'newchat.png')))
        self.new_chat_image.setAlignment(Qt.AlignCenter)
        self.new_chat_image.setToolTip('Your new conversation appears here')
        self.layout.addWidget(self.new_chat_image)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: black;
                background-color: white;
                border-radius: 5px;
                padding: 5px;
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
        self.send_button.setToolTip('Enter Chat')
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
        self.move(screen_geometry.width() - self.width() - 15, screen_geometry.height() - self.height() - 100)

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            self.new_chat_image.hide()
            timestamp = datetime.now().strftime('%I:%M %p')
            self.append_message(user_input, timestamp, align_right=True)
            response = find_best_match(user_input)  # Use original user input for matching
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
            <div style="display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 10px;">
                <div style="background-color: #E8E8E8; color: black; padding: 10px; border-radius: 15px; max-width: 75%; word-wrap: break-word;">
                {message}
                </div>
                <div style="font-size: 14px; color: gray; text-align: right; margin-top: 5px;">{timestamp}</div>
            </div>
        """
        
        bot_style = """
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
                <img src='app/icons/chat.png' width='30' height='30' style="margin-right: 10px; border-radius: 50%;" />
                <div style="background-color: #D7EEF9; color: black; padding: 10px; border-radius: 15px; max-width: 75%; word-wrap: break-word;">
                    <div>{message}</div>
                    <div style="font-size: 14px; color: gray; text-align: left; margin-top: 5px;">{timestamp}</div>
                </div>
            </div>
        """
        
        formatted_message = user_style.format(message=message, timestamp=full_timestamp) if align_right else bot_style.format(message=message, timestamp=full_timestamp)

        self.chat_display.insertHtml(formatted_message)
        self.chat_display.ensureCursorVisible()

    def clear_chat(self, event):
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

    def get_birthday_tooltip(self):
        excel_path = os.path.join('app', 'sqa.xlsx')
        return get_today_birthdays(excel_path)

    def get_anniversary_tooltip(self):
        excel_path = os.path.join('app', 'sqa.xlsx')
        return get_today_anniversaries(excel_path)

    def open_readme(self, event):
        self.readme_dialog = ReadmeDialog()
        self.readme_dialog.exec_()

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
