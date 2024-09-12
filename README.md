# RAG-based PDF Q&A System

This project implements a Retrieval-Augmented Generation (RAG) system for answering questions about PDF documents using a vector database and a Large Language Model (LLM).

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Overview

This system allows users to upload PDF documents, ask questions about their content, and receive accurate answers. It utilizes a vector database for efficient similarity search and provides relevant context to an LLM for generating responses.

## Features

- PDF document ingestion and processing
- Vector representation of document chunks
- Similarity search using a vector database
- Context-aware question answering using an LLM
- User-friendly interface for document upload and querying

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lordlegacy/ragllm.git
   cd ragllm
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the vector database (e.g., Pinecone, Faiss, or Weaviate) following the provider's instructions.

4. Configure the LLM API (e.g., OpenAI GPT-3.5 or GPT-4) by setting the appropriate environment variables.

## Usage

The application exposes several HTTP API endpoints for interacting with the RAG-based PDF Q&A system:

### 1. Upload and Process PDF

Process a PDF document already present on the server.

- **Endpoint:** `POST /upload`
- **Headers:** 
  - `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "pdf_name": "document.pdf"
  }
  ```
- **Response:** JSON object with a success message or error.

### 2. Ask Question

Ask a question about the processed documents.

- **Endpoint:** `POST /ask`
- **Headers:** 
  - `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "question": "What is the main topic?",
    "model": "gpt-3"  // Optional, defaults to "gpt-3"
  }
  ```
- **Response:** JSON object with relevant chunks and the answer.

### 3. Delete Chunks

Delete chunks and embeddings for a specific PDF.

- **Endpoint:** `DELETE /delete`
- **Headers:** 
  - `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "pdf_hash": "hash_value"
  }
  ```
- **Response:** JSON object confirming deletion or error message.

### 4. List Processed PDFs

Retrieve a list of all processed PDF hashes.

- **Endpoint:** `GET /list`
- **Response:** JSON array of processed PDF hashes.

### 5. Health Check

Check if the service is running.

- **Endpoint:** `GET /health`
- **Response:** JSON object with status "OK" if the service is healthy.

## Notes

- Use these API endpoints to interact with the RAG-based PDF Q&A system. 
- You can use any HTTP client (e.g., Postman, cURL, or programming language libraries) to make these requests. 
- Replace the host and port in the URL with the appropriate values where your Flask app is running.
- The system assumes that PDF files are already present in the server's `uploads` directory. The `/upload` endpoint processes these existing files rather than accepting file uploads directly through the API.

## How It Works

1. **Document Ingestion**: The system processes uploaded PDFs, splitting them into manageable chunks.

2. **Vectorization**: Each chunk is converted into a vector representation using a suitable embedding model.

3. **Vector Storage**: The vectors are stored in a vector database for efficient similarity search.

4. **Query Processing**: When a user asks a question, it's converted into a vector representation.

5. **Similarity Search**: The system performs a similarity search in the vector database to find the most relevant document chunks.

6. **Context Retrieval**: The top-k most similar chunks are retrieved as context.

7. **LLM Integration**: The original question and the retrieved context are sent to the LLM.

8. **Answer Generation**: The LLM generates an answer based on the provided context and question.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
