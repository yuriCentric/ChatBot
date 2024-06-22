import spacy
from Rules.rules import get_response

# Load spaCy's English language model
nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('/Training/chatbot_model')

def process_input(user_input):
    # Process the user input with spaCy
    doc = nlp(user_input)
    
    # Get response from rules
    response = get_response(user_input)
    
    return response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = process_input(user_input)
        print(f"Chatbot: {response}")
