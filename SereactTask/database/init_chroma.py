import chromadb
import json
import os
from chroma_crud import expand_embedding

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="product_embeddings")
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "../data/embeddings.json")

with open(file_path, "r") as f:
    embeddings_data = json.load(f)

for item in embeddings_data:
    expanded_embedding = expand_embedding(item["embedding"])
    collection.add(
        ids=[item["id"]],
        embeddings=[expanded_embedding],
        metadatas=[item["metadata"]]
    )
print(f" ChromaDB initialized with {len(embeddings_data)} product metadata entries.")


