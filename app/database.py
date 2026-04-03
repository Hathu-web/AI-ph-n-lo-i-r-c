import os
from pymongo import MongoClient

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

db = client["waste_db"]
collection = db["classification_history"]