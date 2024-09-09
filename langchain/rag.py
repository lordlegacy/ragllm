from store import storage_manager
from embed import embed_chunks
def retrieve_chunk_from_embedding(query_embedding):
    # Search for the closest embedding in Qdrant
    search_result = storage_manager.qdrant_client.search(
        collection_name="pdf_embeddings",
        query_vector=query_embedding.tolist(),  # Convert tensor to list
        limit=1
    )

    # Get the chunk number from the result
    chunk_number = search_result[0].payload["chunk_number"]

    # Retrieve the corresponding chunk text from PostgreSQL
    storage_manager.pg_cursor.execute("SELECT chunk_text FROM pdf_chunks WHERE chunk_number = %s", (chunk_number,))
    result = storage_manager.pg_cursor.fetchone()
    
    return result[0]  # Return the chunk text

# Example usage:
query_embedding = embed_chunks(["Some query text"])
chunk_text = retrieve_chunk_from_embedding(query_embedding)
print(f"Closest chunk: {chunk_text}")
