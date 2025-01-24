import pyttsx3
from threading import Thread

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice to female
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Set speech rate to normal
engine.setProperty('rate', 150)  # You can adjust the number to your preference

# Define the introduction text
introduction_text = """
Welcome! I am CI-Buddy, your intelligent assistant designed to help Centric India employees with a variety of tasks and information. As a newly developed chatbot, just one month into my journey, I am enthusiastic about learning and growing. I am a quick learner and eager to be further trained and refined to better serve your needs.Learn about Centric's history, core values, operations, and HR policies. Access internal sites like payroll, timesheets, learning paths, and the employee portal. Get escalation contacts for IT, Admin, HR, and Leads.Receive helful voice alerts, Use smart keywords adn also you can refer help manual for quick overview of my capabilities.For a hands-free experience, click the voice or mic icon and speak your questions.To summarize, I am here to make your journey at Centric smoother and more efficient. Just ask, and I'll assist you!"""

# Function to play the introduction
def play_introduction():
    def run():
        engine.say(introduction_text)
        engine.runAndWait()
    Thread(target=run).start()

# Function to stop the introduction
def stop_introduction():
    engine.stop()

# Function to get the introduction text
def get_introduction_text():
    return introduction_text
