def get_response(user_input):
    user_input = user_input.lower().strip()
    response = ""
    
    # Greetings
    if any(greeting in user_input for greeting in ['hello', 'hi', 'hey', 'hiya', 'howdy', 'greetings']):
        response += "Hi there! How can I help you? "
    elif any(farewell in user_input for farewell in ['bye', 'goodbye', 'see you', 'take care']):
        response += "Goodbye! Have a great day! "
    elif any(help_query in user_input for help_query in ['help', 'assist', 'support', 'guidance']):
        response += "Sure, I'm here to help! What do you need assistance with? "
    elif 'how are you' in user_input or 'how are you doing' in user_input or 'your name' in user_input:
        response += "I'm just a bot, but I'm here to help! How can I assist you today? "
    elif 'info' in user_input or 'information' in user_input:
        response += "Sure! What information are you looking for? "
    
    # Skill-related queries
    if all(keyword in user_input for keyword in ['when', 'submit', 'certification']):
        response += "The associate must submit their application before the start date of the certification course. "
    elif all(keyword in user_input for keyword in ['who', 'reviews', 'certification']) or all(keyword in user_input for keyword in ['who', 'approves', 'certification']):
        response += "The application is routed to the associate’s Practice Lead and/or CI-Leads (as per the authority matrix) for review, discussion, and approval to ensure its relevance to the associate’s current or potential future role. "
    elif all(keyword in user_input for keyword in ['how', 'long', 'certification']) or all(keyword in user_input for keyword in ['how', 'time', 'certification']):
        response += "All requests will be processed within thirty (30) days of the form submission date. "
    elif all(keyword in user_input for keyword in ['how', 'notified', 'approval', 'certification']) or all(keyword in user_input for keyword in ['how', 'notified', 'denial', 'certification']):

        response +=  "An HR representative will send an email confirmation to the associate upon approval. In case of denial, an email with an explanation for denial will be sent. Denials may be appealed through the HR representative. "
    elif all(keyword in user_input for keyword in ['process', 'approval', 'courses']) or all(keyword in user_input for keyword in ['process', 'approval', 'subscriptions']):
        response +=  "Associates must get courses and subscriptions approved by their Practice Leads before commencement. Post-approval, associates can make the purchase. Reimbursement can be claimed via Open Air upon completion, providing proof of completion and approval emails. "

    # Catch-all response
    if response == "":
        response = "I'm sorry, I don't understand your input. Please drop an email to hr@centricconsulting.com for assistance."

    return response
