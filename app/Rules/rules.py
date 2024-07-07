def get_response(user_input):
    user_input = user_input.lower()
    
    # Greetings
    if any(greeting in user_input for greeting in ['hello', 'hi', 'hey', 'hiya', 'howdy', 'greetings']):
        return "Hi there! How can I help you?"

    # Farewells
    elif any(farewell in user_input for farewell in ['bye', 'goodbye', 'see you', 'take care']):
        return "Goodbye! Have a great day!"

    # Asking for help or assistance
    elif any(help_query in user_input for help_query in ['help', 'assist', 'support', 'guidance']):
        return "Sure, I'm here to help! What do you need assistance with?"

    # Asking about the day
    elif 'how are you' in user_input or 'how are you doing' in user_input or 'your name' in user_input:
        return "I'm just a bot, but I'm here to help! How can I assist you today?"

    # Asking for information
    elif 'info' in user_input or 'information' in user_input:
        return "Sure! What information are you looking for?"

    # Catch-all response
    else:
        return "I'm sorry, I don't understand your input. Please drop an email to hr@centricconsulting.com for assistance."

