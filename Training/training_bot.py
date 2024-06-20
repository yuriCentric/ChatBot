import pandas as pd
import spacy
from spacy.training.example import Example

# Load training data
data = pd.read_excel('data/training_data.xlsx')

# Convert data into a list of tuples
training_data = [(row['Intent'], row['Response']) for index, row in data.iterrows()]

# Initialize a blank English model
nlp = spacy.blank("en")

# Define the components of the pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner, last=True)

# Add labels to the NER component
for _, annotations in training_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Start the training
nlp.begin_training()

# Prepare training examples
examples = []
for text, annotations in training_data:
    examples.append(Example.from_dict(nlp.make_doc(text), annotations))

# Train the model
for i in range(10):
    random.shuffle(examples)
    for example in examples:
        nlp.update([example])

        # Save the model
nlp.to_disk("chatbot_model")

# Load the model in your application
nlp = spacy.load("chatbot_model")

