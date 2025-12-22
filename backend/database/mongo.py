from pymongo import MongoClient
from backend.config import settings

client = MongoClient(settings.MONGODB_URI)
db = client["chatApplication"]  # Database name
rooms_collection = db["rooms"]