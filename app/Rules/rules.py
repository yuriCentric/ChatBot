def get_response(user_input):
    # Simple rule-based responses
    if "hello" in user_input.lower():
        return "Hi there! How can I help you?"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I am sorry, I don't understand that."
