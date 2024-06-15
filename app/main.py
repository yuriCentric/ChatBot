import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton
from chat_bot import get_response

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.setWindowTitle('Chatbot')
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.input_box = QLineEdit(self)
        self.layout.addWidget(self.input_box)

        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def send_message(self):
        user_input = self.input_box.text()
        if user_input:
            self.chat_display.append(f"You: {user_input}")
            response = get_response(user_input)
            self.chat_display.append(f"Chatbot: {response}")
            self.input_box.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot_app = ChatbotApp()
    chatbot_app.show()
    sys.exit(app.exec_())
