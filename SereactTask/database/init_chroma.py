import chromadb
import json

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="product_embeddings")

with open("../data/embeddings.json","r") as f:
    embeddings_data = json.load(f)

for item in embeddings_data:
    collection.add(ids=[item["id"]], embeddings=[item["embedding"]], metadatas=[item["metadata"]])
print("ChromaDb initialized with product metadata.")
