import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = "car_wash"

client = pymongo.MongoClient(MONGO_URI)
mongo_db = client[MONGO_DB_NAME]

permissions_collection = mongo_db["permissions"]
subscriptions_collection = mongo_db["subscriptions"]
users_collection = mongo_db["users"]
