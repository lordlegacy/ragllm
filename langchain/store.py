from embed import embed_chunks  # Your existing embedding function
from process_pdf import chunk_pdf  # Your existing PDF chunking function
from storage_module import StorageManager  # The storage module we created

# Configuration for PostgreSQL
pg_config = {
    'dbname': 'your_db_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}

# Initialize the storage manager
storage_manager = StorageManager(pg_config)

# Load your PDF, chunk it, and embed the chunks
pdf_file_path = "m.pdf"
chunks = chunk_pdf(pdf_file_path, chunk_size=500)
embeddings = embed_chunks(chunks)

# Store each chunk and its embedding in PostgreSQL and Qdrant
for i, chunk_text in enumerate(chunks):
    embedding = embeddings[i]  # Get the corresponding embedding
    storage_manager.store_chunk(chunk_number=i, chunk_text=chunk_text, embedding=embedding)

# Close the storage manager when done
storage_manager.close()
