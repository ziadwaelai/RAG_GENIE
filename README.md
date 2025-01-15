# GENIE

GENIE AI is a Streamlit-based web application for talent acquisition and resume analysis, leveraging AI to process, analyze, and interact with uploaded resumes in PDF format. This application supports hybrid search functionality, document vectorization, and conversational AI capabilities.

---

## Features

- **PDF Upload**: Upload and validate multiple PDF files.
- **Context Retrieval**: Extract and store resume data using vector embeddings.
- **Chat Interface**: Interact with an AI assistant for resume analysis and talent acquisition tasks.
- **Hybrid Search**: Combines BM25 and semantic retrieval methods for context.
- **Streaming Responses**: Supports real-time, streaming AI-generated responses.
- **Dockerized Setup**: Simplified deployment using Docker Compose.

---

## Project Structure

```plaintext
.
├── api/                    # Backend API for processing requests
├── chatbot/                # Chatbot configuration and templates
├── docs/                   # Document utilities and retrievers
├── docker/                 # Docker configuration files
├── pdfs/                   # Uploaded PDF files
├── db/                     # Persisted vector store
├── requirements.txt        # Python dependencies
├── Dockerfile.api          # Dockerfile for API service
├── Dockerfile.main         # Dockerfile for main service
├── docker-compose.yml      # Docker Compose configuration
├── helper.py               # Utility functions for file validation and formatting
└── main.py                 # Streamlit application entry point
```

---

## Prerequisites

Ensure the following tools are installed on your system:

- Docker
- Docker Compose
- Python 3.11 or higher

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Build and Run with Docker Compose

Build and start the application using Docker Compose:

```bash
docker-compose up --build
```

This will:
- Start the `ollama` container for the AI model.
- Start the `api` container for backend services.
- Start the `main` container for the Streamlit frontend.

Access the application at `http://localhost:8501`.

---

## Components

### **Streamlit Frontend**
- Provides a user-friendly interface for uploading PDFs and interacting with the AI chatbot.

### **FastAPI Backend**
- Handles file uploads, vectorization, and hybrid retrieval logic.

### **Hybrid Search**
- Combines BM25 and vector-based semantic retrieval for enhanced document relevance.

### **Vector Store**
- Persisted using Chroma for efficient context retrieval.

---

## How to Use

1. **Upload Resumes**:
   - Use the sidebar to upload PDF files.
   - Valid files are stored, and errors are displayed for invalid files.

2. **Interact with the Chatbot**:
   - Ask questions about the uploaded resumes.
   - View streaming AI responses directly in the chat interface.

3. **Advanced Features**:
   - The backend processes resumes into vector embeddings for quick retrieval.
   - Hybrid search ensures contextually relevant results.

---

## Environment Variables

The following environment variables are configurable:

| Variable       | Default Value               | Description                          |
|----------------|-----------------------------|--------------------------------------|
| `PYTHONPATH`   | `/app`                      | Path to the application files.       |
| `OLLAMA_HOST`  | `http://ollama:11434`       | Host address for the Ollama service. |

---

## File Upload Validation

- **Accepted Format**: PDF only.
- **Maximum Size**: 20MB.
- Files are validated upon upload, and errors are displayed for unsupported formats or oversized files.

---

## Development

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

1. Start the backend API:

   ```bash
   python api.py
   ```

2. Start the Streamlit frontend:

   ```bash
   streamlit run main.py
   ```

---


## Acknowledgments

This project uses the following tools and libraries:

- **Streamlit**: Frontend framework.
- **FastAPI**: Backend API framework.
- **LangChain**: Document processing and retrieval.
- **Chroma**: Vector store.
- **BM25**: Keyword-based retrieval.
- **Ollama**: AI model hosting.
- **Docker**: Containerization.
