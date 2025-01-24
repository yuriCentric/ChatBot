from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from datetime import datetime, time
import threading
import psutil
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def voice_alert(message):
    engine.say(message)
    if not engine._inLoop:
        engine.runAndWait()

class ReminderDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Important: Timesheet Reminder")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(open('app/css/alerts.css').read())

        layout = QVBoxLayout()
        label = QLabel("Have you submitted your timesheet today?")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        yes_button.clicked.connect(self.accept)
        no_button.clicked.connect(self.reject)
        self.setGeometry(1450, 170, 400, 100)

def show_reminder_popup():
    dialog = ReminderDialog()
    dialog.exec_()
    if dialog.result() == QDialog.Rejected:
        return "Hi, it's important to submit your timesheet today. You can do it here: https://auth.openair.com/"

def check_reminder_time():
    now = datetime.now()
    if now.weekday() == 2:
        reminder_times = [time(12, 50), time(14, 35)]
        for reminder_time in reminder_times:
            if now.time().replace(second=0, microsecond=0) == reminder_time:
                threading.Thread(target=voice_alert, args=("Have you submitted your timesheet today?",)).start()
                return show_reminder_popup()
    return None

class BatteryChecker(QObject):
    battery_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self.check_battery)
        self.battery_timer.start(10000)

    def check_battery(self):
        battery = psutil.sensors_battery()
        if battery is not None:
            if battery.percent >= 70 and battery.power_plugged:
                self.battery_signal.emit("Battery is full. Please unplug the charger.")
            elif battery.percent <= 20 and not battery.power_plugged:
                self.battery_signal.emit("Battery is low. Please plug in the charger.")

class BatteryAlert(QObject):
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.battery_checker = BatteryChecker()
        self.battery_checker.moveToThread(self.thread)
        self.battery_checker.battery_signal.connect(voice_alert)
        self.thread.started.connect(self.start_timer)
        self.thread.start()

    def start_timer(self):
        self.battery_checker.battery_timer.start(30000)

# Example usage of BatteryAlert
battery_alert = BatteryAlert()
