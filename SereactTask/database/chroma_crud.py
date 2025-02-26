import chromadb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
DB_PATH = os.path.join(BASE_DIR, "../database/chroma_db")  # Adjust path to point to the database folder

# Ensure the directory exists
os.makedirs(DB_PATH, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="product_embeddings")


# CREATE: Insert a new embedding
def add_embedding(product_id, embedding, metadata):
    new_embedding = expand_embedding(embedding)
    collection.add(ids=[product_id], embeddings=[new_embedding], metadatas=[metadata])
    return f"Added embedding for product ID: {product_id}"


# READ: Retrieve embeddings (nearest neighbor search)
def search_embeddings(query_embedding, n_results=10):
    print("seeing")
    print(collection.count())  # Should return a non-zero value

    print(collection.peek())
    similar_products = collection.query(query_embedding, n_results=10)
    return similar_products


# UPDATE: Modify existing embeddings (ChromaDB doesn't support updates directly)
def update_embedding(product_id, new_embedding, new_metadata):
    collection.delete(ids=[product_id])
    embedding = expand_embedding(new_embedding)
    collection.add(ids=[product_id], embeddings=[embedding], metadatas=[new_metadata])
    return f"Updated embedding for product ID: {product_id}"


# DELETE: Remove an embedding
def delete_embedding(product_id):
    collection.delete(ids=[product_id])
    return f"Deleted embedding for product ID: {product_id}"


def expand_embedding(embedding, target_dim=768):
    """Expands the embedding to the target dimension by zero padding."""
    return embedding + [0.0] * (target_dim - len(embedding))
