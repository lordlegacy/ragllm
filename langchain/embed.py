# embedding_local.py
from sentence_transformers import SentenceTransformer
from process_pdf import chunk_pdf  # Importing the chunking module for chunking PDFs

# Load the model locally
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_chunks(chunks):
    """
    Embeds the given chunks using a locally loaded sentence-transformers model.
    
    Parameters:
    - chunks (list of str): List of text chunks to embed.
    
    Returns:
    - List of embeddings for each chunk.
    """
    # Generate embeddings for all chunks in a single batch
    embeddings = model.encode(chunks, convert_to_tensor=False)
    return embeddings

if __name__ == "__main__":
    # Example usage
    pdf_file_path = "m.pdf"  # Path to the PDF file
    
    # Use the chunk_pdf function from chunking.py to get text chunks
    chunks = chunk_pdf(pdf_file_path, chunk_size=500)
    
    # Embed the chunks using the locally loaded model
    embeddings = embed_chunks(chunks)
    
    # Output the embeddings (you can store them in a database if needed)
    for idx, embedding in enumerate(embeddings):
        print(f"Embedding {idx + 1}: {embedding[:5]}... [truncated]")
