import hashlib
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct

class StorageManager:
    def __init__(self, pg_config, qdrant_host="localhost", qdrant_port=6333):
        self.pg_conn = psycopg2.connect(**pg_config)
        self.pg_cursor = self.pg_conn.cursor()
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

    # Method to generate hash for a PDF file
    def generate_pdf_hash(self, pdf_file_path):
        hasher = hashlib.md5()  # You can use sha256() for stronger hashing
        with open(pdf_file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    # Method to check if the PDF hash exists in the database
    def is_pdf_processed(self, pdf_hash):
        self.pg_cursor.execute("SELECT 1 FROM pdf_hashes WHERE pdf_hash = %s;", (pdf_hash,))
        return self.pg_cursor.fetchone() is not None

    # Store the hash of the PDF
    def store_pdf_hash(self, pdf_hash):
        try:
            self.pg_cursor.execute(
                "INSERT INTO pdf_hashes (pdf_hash) VALUES (%s);",
                (pdf_hash,)
            )
            self.pg_conn.commit()
        except Exception as e:
            print(f"Error inserting PDF hash into PostgreSQL: {e}")
            self.pg_conn.rollback()

    # Create Qdrant collection for embeddings
    def create_qdrant_collection(self):
        self.qdrant_client.recreate_collection(
            collection_name="pdf_embeddings",
            vectors_config=VectorParams(size=384, distance="Cosine")
        )

    # Store chunk text in PostgreSQL and embedding in Qdrant
    def store_chunk(self, chunk_number, chunk_text, embedding):
        # Insert into PostgreSQL
        try:
            self.pg_cursor.execute(
                "INSERT INTO pdf_chunks (chunk_number, chunk_text) VALUES (%s, %s);",
                (chunk_number, chunk_text)
            )
            self.pg_conn.commit()
        except Exception as e:
            print(f"Error inserting into PostgreSQL: {e}")
            self.pg_conn.rollback()

        # Insert embedding into Qdrant
        try:
            self.qdrant_client.upsert(
                collection_name="pdf_embeddings",
                points=[PointStruct(
                    id=chunk_number,
                    vector=embedding.tolist(),
                    payload={"chunk_number": chunk_number}
                )]
            )
        except Exception as e:
            print(f"Error inserting into Qdrant: {e}")

    # Retrieve the chunk of text based on embedding
    def retrieve_chunk_from_embedding(self, query_embedding):
        # Search for the closest embedding in Qdrant
        search_result = self.qdrant_client.search(
            collection_name="pdf_embeddings",
            query_vector=query_embedding.tolist(),
            limit=1
        )

        # Get the chunk number from the result
        chunk_number = search_result[0].payload["chunk_number"]

        # Retrieve the corresponding chunk text from PostgreSQL
        self.pg_cursor.execute("SELECT chunk_text FROM pdf_chunks WHERE chunk_number = %s", (chunk_number,))
        result = self.pg_cursor.fetchone()

        return result[0] if result else None

    # Close PostgreSQL connection
    def close(self):
        self.pg_cursor.close()
        self.pg_conn.close()
