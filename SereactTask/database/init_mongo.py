from pymongo import MongoClient
import json
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["product_db"]
collection = db["products"]
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "../data/products.json")

with open(file_path,"r") as f:
    products_data = json.load(f)

collection.insert_many(products_data)
print(f" MongoDB initialized with {len(products_data)} product metadata entries.")
