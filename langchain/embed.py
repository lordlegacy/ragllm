from sentence_transformers import SentenceTransformer
import torch

# Set up device for embedding model (GPU if available)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the model once and reuse it
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=device)

def embed_chunks(chunks, batch_size=32):
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = model.encode(batch_chunks, convert_to_tensor=False)
        embeddings.extend(batch_embeddings)
    return embeddings
