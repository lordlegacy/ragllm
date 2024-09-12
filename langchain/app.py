import os
import time
import openai
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from storage_manager import StorageManager
from process_pdf import chunk_pdf
from embed import embed_chunks, openai_embed_chunks
from config import Config

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Storage Manager instance
storage_manager = StorageManager(
    pg_config={
        'dbname': Config.POSTGRES_DB,
        'user': Config.POSTGRES_USER,
        'password': Config.POSTGRES_PASSWORD,
        'host': Config.POSTGRES_HOST,
        'port': Config.POSTGRES_PORT
    },
    qdrant_host="localhost",
    qdrant_port=6333
)

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API route to upload and process a PDF by name
@app.route('/upload', methods=['POST'])
def upload_pdf():
    data = request.get_json()
    pdf_name = data.get('pdf_name', None)

    if not pdf_name:
        return jsonify({"error": "PDF name is required"}), 400

    # Construct the file path based on the provided name
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "PDF file does not exist on the server"}), 400

    # Check if the PDF has already been processed
    pdf_hash = storage_manager.generate_pdf_hash(file_path)
    if storage_manager.is_pdf_processed(pdf_hash):
        return jsonify({"message": "This PDF has already been processed."}), 200

    # Process the PDF
    try:
        process_and_store_pdf(file_path)
        storage_manager.store_pdf_hash(pdf_hash)
        return jsonify({"message": "PDF processed and stored successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to ask a question and retrieve the answer
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question", None)
    model_name = data.get("model", "gpt-3")  # Allow model selection

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Embed the question using OpenAI embeddings
    try:
        query_embedding = openai_embed_chunks([question])[0]

        # Retrieve 3 closest chunks
        results = storage_manager.retrieve_multiple_chunks_from_embedding(query_embedding, limit=3)
        chunks = [result['chunk_text'] for result in results]

        # Pass the question and chunks to the selected LLM (e.g., GPT-3)
        if model_name == "gpt-3":
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Question: {question}\nRelevant Information: {chunks}\nAnswer:",
                max_tokens=150
            )
            answer = response.choices[0].text.strip()
        else:
            # Default to GPT-3 or handle other models
            answer = "Selected model is not supported yet."

        return jsonify({"chunks": chunks, "answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to delete a PDF's chunks and embeddings based on the PDF hash
@app.route('/delete', methods=['DELETE'])
def delete_chunks():
    data = request.get_json()
    pdf_hash = data.get("pdf_hash", None)

    if not pdf_hash:
        return jsonify({"error": "PDF hash is required"}), 400

    # Delete chunks and embeddings by the PDF hash
    try:
        storage_manager.pg_cursor.execute("DELETE FROM pdf_chunks WHERE pdf_hash = %s;", (pdf_hash,))
        storage_manager.pg_conn.commit()
        return jsonify({"message": "Chunks and embeddings deleted."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to list all processed PDFs
@app.route('/list', methods=['GET'])
def list_processed_pdfs():
    try:
        storage_manager.pg_cursor.execute("SELECT pdf_hash FROM pdf_hashes;")
        result = storage_manager.pg_cursor.fetchall()
        processed_pdfs = [row[0] for row in result]
        return jsonify({"processed_pdfs": processed_pdfs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route for health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# Helper function to process and store PDF
def process_and_store_pdf(pdf_file_path):
    # Step 1: Chunk the PDF
    start_time = time.time()
    chunks = chunk_pdf(pdf_file_path)
    print(f"Time to chunk PDF: {time.time() - start_time:.2f} seconds")

    # Step 2: Create Qdrant collection
    storage_manager.create_qdrant_collection()

    # Step 3: Embed the chunks
    start_time = time.time()
    embeddings = embed_chunks(chunks)
    print(f"Time to generate embeddings: {time.time() - start_time:.2f} seconds")

    # Step 4: Store chunks and embeddings in PostgreSQL and Qdrant
    start_time = time.time()
    for i, chunk_text in enumerate(chunks):
        embedding = embeddings[i]
        storage_manager.store_chunk(i, chunk_text, embedding)
    print(f"Time to store chunks and embeddings: {time.time() - start_time:.2f} seconds")

# Run the Flask app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5000)
