import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="product_embeddings")


# CREATE: Insert a new embedding
def add_embedding(product_id, embedding, metadata):
    collection.add(ids=[product_id], embeddings=[embedding], metadatas=[metadata])
    return f"Added embedding for product ID: {product_id}"


# READ: Retrieve embeddings (nearest neighbor search)
def search_embeddings(query_embedding, n_results=5):
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results


# UPDATE: Modify existing embeddings (ChromaDB doesn't support updates directly)
def update_embedding(product_id, new_embedding, new_metadata):
    collection.delete(ids=[product_id])
    collection.add(ids=[product_id], embeddings=[new_embedding], metadatas=[new_metadata])
    return f"Updated embedding for product ID: {product_id}"


# DELETE: Remove an embedding
def delete_embedding(product_id):
    collection.delete(ids=[product_id])
    return f"Deleted embedding for product ID: {product_id}"
