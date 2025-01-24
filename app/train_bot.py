import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("sys.path:", sys.path)

try:
    from pymongo import MongoClient, UpdateOne
    print("pymongo is installed correctly.")
except ModuleNotFoundError:
    print("pymongo is not installed.")
    sys.exit(1)

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, EXCEL_FILE_PATH

def insert_data_to_mongodb(file_path, db_name, collection_name, connection_string):
    df = pd.read_excel(file_path)
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    operations = []
    for _, row in df.iterrows():
        operations.append(
            UpdateOne(
                {'input': row['input']},
                {'$set': {'input': row['input'], 'response': row['response']}},
                upsert=True
            )
        )

    if operations:
        result = collection.bulk_write(operations)
        print(f"Data inserted/updated in MongoDB database: {db_name}, collection: {collection_name}")
        print(f"Inserted: {result.upserted_count}, Modified: {result.modified_count}")

def train_bot_from_mongodb(db_name, collection_name, connection_string):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    training_data = collection.find()

    bot = ChatBot('MyBot', storage_adapter='chatterbot.storage.MongoDatabaseAdapter', database_uri=connection_string)
    trainer = ListTrainer(bot)

    training_pairs = []
    for data in training_data:
        training_pairs.append(data['input'])
        training_pairs.append(data['response'])

    trainer.train(training_pairs)
    print("Bot training completed.")

    return bot

if __name__ == "__main__":
    insert_data_to_mongodb(EXCEL_FILE_PATH, DB_NAME, COLLECTION_NAME, MONGO_URI)
    bot = train_bot_from_mongodb(DB_NAME, COLLECTION_NAME, MONGO_URI)

    response = bot.get_response("Your query here")
    print(response)
