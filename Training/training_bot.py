import random
import pandas as pd
import spacy
from spacy.training.example import Example

# Load training data from an Excel file
data = pd.read_excel('data/training_data.xlsx')

# Convert data into a list of tuples
training_data = []
for index, row in data.iterrows():
    text = row['Text']
    entities = eval(row['Entities'])  # Use eval to convert string representation of list to a list
    training_data.append((text, {"entities": entities}))

# Initialize a blank English model
nlp = spacy.blank("en")

# Define the components of the pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)

# Add labels to the NER component
for _, annotations in training_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other pipelines for training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  # Only train NER
    optimizer = nlp.begin_training()
    for itn in range(100):  # Number of training iterations
        random.shuffle(training_data)
        losses = {}
        batches = spacy.util.minibatch(training_data, size=spacy.util.compounding(4.0, 32.0, 1.001))
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.5, losses=losses)
        print("Losses", losses)

# Save the trained model
nlp.to_disk("chatbot_model")
