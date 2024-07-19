import pandas as pd
from datetime import datetime

def get_today_birthdays(excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Get today's date
    today = datetime.today()

    # Filter rows where DOB matches today's date
    birthdays_today = df[df['DOB'].dt.month == today.month]
    birthdays_today = birthdays_today[birthdays_today['DOB'].dt.day == today.day]

    if birthdays_today.empty:
        return "No birthdays today."
    else:
        birthday_messages = []
        for _, row in birthdays_today.iterrows():
            name = row['Employee Name']
            birthday_messages.append(f'{name}')
        return "Today's Birthdays:\n" + "\n".join(birthday_messages)

def get_today_anniversaries(excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Get today's date
    today = datetime.today()

    # Filter rows where DOJ matches today's month and day
    anniversaries_today = df[df['DOJ'].dt.month == today.month]
    anniversaries_today = anniversaries_today[anniversaries_today['DOJ'].dt.day == today.day]

    if anniversaries_today.empty:
        return "No work anniversaries today."
    else:
        anniversary_messages = []
        for _, row in anniversaries_today.iterrows():
            years = today.year - row['DOJ'].year
            name = row['Employee Name']
            anniversary_messages.append(f'{name} {years}yrs anniversary')
        return "Today's Work Anniversaries:\n" + "\n".join(anniversary_messages)

def get_email_by_name(excel_path, name):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Find the email by name
    person = df[df['Employee Name'].str.contains(name, case=False, na=False)]

    if not person.empty:
        return person['Email'].values[0]
    else:
        return None
