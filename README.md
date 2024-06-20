# how to setup:

cd ChatBot
python -m venv nv
source env/bin/activate # On Windows, use `env\Scripts\activate`

pip install spacy
pip install pyqt5
pip install pandas
pip install openpyxl

python -m spacy download en_core_web_sm

# You can now load the package via spacy.load('en_core_web_sm')

# Other way:

pip install -r requirements.txt

# how to run:

cd ChatBot/app
python main.py
