import spacy
from textblob import TextBlob
import traceback

# Load spaCy's English language model
nlp = spacy.load('en_core_web_sm')

# Predefined responses for common inputs
predefined_responses = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What can I do for you?",
    "hey": "Hey! How's it going?",
    "good morning": "Good morning! How can I help you?",
    "good afternoon": "Good afternoon! What can I do for you?",
    "good evening": "Good evening! How can I assist you today?",
    "how are you": "I'm just a bot, but I'm here to help you. How can I assist you today?",
    "what is your name": "I'm Centric Buddy, your personal assistant.",
    "thank you": "You're welcome! If you have any other questions, feel free to ask.",
    "thanks": "You're welcome! If you have any other questions, feel free to ask.",
    "bye": "Goodbye! Have a great day!",
}

def get_entities(doc):
    return [(ent.text, ent.label_) for ent in doc.ents]

def get_pos_tags(doc):
    return [(token.text, token.pos_) for token in doc]

def get_dependencies(doc):
    return [(token.text, token.dep_, token.head.text) for token in doc]

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

def get_word_embeddings(doc):
    return {token.text: token.vector for token in doc}

def get_response(user_input):
    try:
        # Check for predefined responses first
        lower_input = user_input.lower().strip()
        if lower_input in predefined_responses:
            return predefined_responses[lower_input]
        
        # If no predefined response, perform NLP processing
        doc = nlp(user_input)
        
        # Extract NLP features
        entities = get_entities(doc)
        pos_tags = get_pos_tags(doc)
        dependencies = get_dependencies(doc)
        sentiment = analyze_sentiment(user_input)
        embeddings = get_word_embeddings(doc)
        
        # Fallback response for unrecognized inputs
        fallback_response = "I'm sorry, I don't understand. Please drop an email to hr@centricconsulting.com."
        
        # Generate a response based on the input
        response = fallback_response
        
        # Example logic based on detected entities or POS tags
        if entities or pos_tags:
            response = f"Entities: {entities}\nPOS Tags: {pos_tags}"
        else:
            response = "I'm sorry, I couldn't detect any meaningful entities or POS tags in your input."
        
        return response
    
    except Exception as e:
        traceback.print_exc()
        return "I encountered an error. Please try again later."

def process_input(user_input):
    try:
        # Perform NLP processing
        doc = nlp(user_input)

        # Check for specific conditions or keywords
        if any(token.text.lower() in ['hello', 'hi', 'hey'] for token in doc):
            response = "Hello! How can I help you today?"
        elif any(token.text.lower() in ['how', 'are', 'you'] for token in doc):
            response = "I'm just a chatbot, but I'm here to assist you!"
        else:
            response = "I'm sorry, I don't understand your input. Please drop an email to hr@centricconsulting.com for assistance."

        return response
    
    except Exception as e:
        print(f"Error processing input: {e}")
        return "I encountered an error. Please try again later."