from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["product_db"]
collection = db["products"]


# CREATE: Insert a new product
def create_product(product_data):
    result = collection.insert_one(product_data)
    return f"Inserted product with ID: {result.inserted_id}"


# READ: Get a product by ID
def get_product(product_id):
    return collection.find_one({"_id": product_id})


# UPDATE: Update a product's details
def update_product(product_id, update_data):
    result = collection.update_one({"_id": product_id}, {"$set": update_data})
    return f"Modified {result.modified_count} document(s)"


# DELETE: Remove a product by ID
def delete_product(product_id):
    result = collection.delete_one({"_id": product_id})
    return f"Deleted {result.deleted_count} document(s)"
