import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path

dotenv_path = Path('./server/mongodb/test/.env')
load_dotenv(dotenv_path=dotenv_path)

MONGODB_HOST = os.getenv("MONGODB_HOST")
# print(type(os.getenv("MONGODB_PORT")))
MONGODB_PORT = int(os.getenv("MONGODB_PORT"))
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

client = MongoClient()

client = MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/?authMechanism=DEFAULT&authSource={MONGODB_DBNAME}")

db = client[MONGODB_DBNAME]

for collection in db.list_collection_names():
    print(collection)
