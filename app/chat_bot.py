import spacy
from textblob import TextBlob
from Rules.rules import get_response

# Load spaCy's English language model
nlp = spacy.load('en_core_web_sm')

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

def process_input(user_input):
    try:
         # Perform NLP processing
        doc = nlp(user_input)
        return get_response(user_input);
    
    except Exception as e:
        print(f"Error processing input: {e}")
        return "I encountered an error. Please try again later."