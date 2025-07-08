from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

def insert_event(data):
    collection.insert_one(data)

def get_latest_events(limit=10):
    return list(collection.find().sort("timestamp", -1).limit(limit))
