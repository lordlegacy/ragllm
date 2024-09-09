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