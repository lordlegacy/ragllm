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

1. Start the application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Upload a PDF document using the provided interface.

4. Ask questions about the document in the query box.

5. View the generated answers along with the relevant context.

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
