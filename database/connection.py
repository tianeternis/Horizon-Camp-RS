import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def connect_to_database(): 
    client = MongoClient(MONGODB_URI)
    db = client.get_database(DATABASE_NAME)
    return db