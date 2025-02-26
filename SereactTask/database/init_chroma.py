import chromadb
import json
from chroma_crud import expand_embedding

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="product_embeddings")

with open("../data/embeddings.json", "r") as f:
    embeddings_data = json.load(f)

for item in embeddings_data:
    expanded_embedding = expand_embedding(item["embedding"])
    collection.add(
        ids=[item["id"]],
        embeddings=[expanded_embedding],
        metadatas=[item["metadata"]]
    )
print("ChromaDb initialized with product metadata.")



