from embed import embed_chunks  # Your existing embedding function
from process_pdf import chunk_pdf  # Your existing PDF chunking function
from storage_module import StorageManager  # The storage module we created
import time
# Configuration for PostgreSQL
pg_config = {
    'dbname': 'ragllm',
    'user': 'postgres',
    'password': 'wearelegion',
    'host': 'localhost',
    'port': '5432'
}

# Initialize the storage manager
storage_manager = StorageManager(pg_config)

def process_and_store_pdf(pdf_file_path):
    from embed import embed_chunks
    from process_pdf import chunk_pdf

    # Create a Qdrant collection
    storage_manager.create_qdrant_collection()

    # Load your PDF, chunk it, and embed the chunks
    chunks = chunk_pdf(pdf_file_path, chunk_size=500)
    embeddings = embed_chunks(chunks)

    # Store each chunk and its embedding
    for i, chunk_text in enumerate(chunks):
        embedding = embeddings[i]
        storage_manager.store_chunk(chunk_number=i, chunk_text=chunk_text, embedding=embedding)

if __name__ == "__main__":
    process_and_store_pdf("m.pdf")
