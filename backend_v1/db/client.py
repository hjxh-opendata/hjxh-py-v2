from pymongo import MongoClient

from .config import MONGO_URI, MONGO_DATABASE_NAME

client = MongoClient(MONGO_URI)

db = client[MONGO_DATABASE_NAME]
