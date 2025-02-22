from pymongo import MongoClient
import json
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["product_db"]
collection = db["products"]

with open("../data/products.json","r") as f:
    products_data = json.load(f)

collection.insert_many(products_data)
print("MongoDB initialized with product metadata.")
