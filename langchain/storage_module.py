import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import  VectorParams, PointStruct

# Connect to PostgreSQL and Qdrant
class StorageManager:
    def __init__(self, pg_config, qdrant_host="localhost", qdrant_port=6333):
        # PostgreSQL connection
        self.pg_conn = psycopg2.connect(**pg_config)
        self.pg_cursor = self.pg_conn.cursor()
        
        # Qdrant client connection
        self.qdrant_client = QdrantClient(qdrant_host, port=qdrant_port)

    # Create Qdrant collection if it doesn't exist
    def create_qdrant_collection(self):
        self.qdrant_client.recreate_collection(
            collection_name="pdf_embeddings",
            vectors_config=VectorParams(size=384, distance="Cosine"),
        )
    
    # Store chunk text in PostgreSQL and embedding in Qdrant
    def store_chunk(self, chunk_number, chunk_text, embedding):
        # 1. Insert chunk text into PostgreSQL
        try:
            self.pg_cursor.execute(
                "INSERT INTO pdf_chunks (chunk_number, chunk_text) VALUES (%s, %s);",
                (chunk_number, chunk_text)
            )
            self.pg_conn.commit()
        except Exception as e:
            print(f"Error inserting into PostgreSQL: {e}")
            self.pg_conn.rollback()
        
        # 2. Insert embedding into Qdrant
        try:
            self.qdrant_client.upsert(
                collection_name="pdf_embeddings",
                points=[
                    PointStruct(
                        id=chunk_number,  # Same chunk number as the primary key
                        vector=embedding.tolist(),  # Convert embedding to list
                        payload={"chunk_number": chunk_number}
                    )
                ]
            )
        except Exception as e:
            print(f"Error inserting into Qdrant: {e}")

    # Close the PostgreSQL connection when done
    def close(self):
        self.pg_cursor.close()
        self.pg_conn.close()

