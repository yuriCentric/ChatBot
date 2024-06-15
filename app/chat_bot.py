import spacy

# Load spaCy's English language model
nlp = spacy.load('en_core_web_sm')

def get_response(user_input):
    # Process the user input
    doc = nlp(user_input)
    
    # Simple rule-based responses
    if "hello" in user_input.lower():
        return "Hi there! How can I help you?"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I am sorry, I don't understand that."

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = get_response(user_input)
        print(f"Chatbot: {response}")
