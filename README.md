# how to setup:

cd ChatBot
python -m venv env
source env/bin/activate # On Windows, use `env\Scripts\activate`

pip install spacy
pip install pyqt5
pip install pandas
pip install openpyxl
pip install psutil
pip install pyttsx3
pip install textblob

python -m spacy download en_core_web_sm

# You can now load the package via spacy.load('en_core_web_sm')

# Other way:

pip install -r requirements.txt

# how to run:

cd ChatBot/app
python main.py
____________________________
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned 
-Scope Process
env\Scripts\activate
"c:/Users/sagar.patel/OneDrive - Centric Consulting/Documents/GitHub/ChatBot/env/Scripts/python.exe" "c:/Users/sagar.patel/OneDrive - Centric Consulting/Documents/GitHub/ChatBot/app/main.py"