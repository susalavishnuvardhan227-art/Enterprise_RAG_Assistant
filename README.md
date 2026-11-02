# Enterprise RAG Assistant

An AI-powered document question-answering application built using Retrieval-Augmented Generation (RAG). It allows users to upload PDF documents, retrieve relevant information through semantic search, and generate context-based answers using a locally running Large Language Model.

## Overview

Enterprise RAG Assistant is a local document intelligence prototype designed to demonstrate how organizations can retrieve information from internal documents using AI.

The application combines PDF processing, text chunking, semantic embeddings, vector search, and LLM-based answer generation.

## Features

- Multiple PDF document uploads
- PDF text extraction using PyMuPDF
- Text chunking with configurable overlap
- Semantic embeddings using Sentence Transformers
- Vector storage and retrieval using ChromaDB
- Context-based answer generation using Qwen 2.5 3B
- Local LLM execution through Ollama
- Source document and page references
- Retrieval and generation performance timings
- Basic custom retrieval evaluation
- Streamlit-based dashboard

## Application Modules

The dashboard contains five sections:

1. System Overview
2. Knowledge Base
3. Knowledge Search
4. Evaluation Centre
5. System Settings

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| PDF Processing | PyMuPDF |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Framework | Sentence Transformers |
| Vector Database | ChromaDB |
| Large Language Model | Qwen 2.5 3B |
| LLM Runtime | Ollama |

## RAG Architecture

```text
              PDF Documents
                    |
                    v
             PDF Text Extraction
                    |
                    v
               Text Chunking
                    |
                    v
             MiniLM Embeddings
                    |
                    v
                ChromaDB
                    |
                    |
User Question ------+
       |
       v
Question Embedding
       |
       v
Semantic Retrieval
       |
       v
Relevant Document Chunks
       |
       v
     RAG Prompt
       |
       v
   Qwen 2.5 3B
       |
       v
 Generated Answer
       |
       v
 Answer + Source References
```

## Project Structure

```text
Enterprise_RAG_Assistant/
|
|-- app.py
|-- rag_engine.py
|-- search.py
|-- ingest.py
|-- chunker.py
|-- document_loader.py
|-- embedding_generator.py
|-- vector_database.py
|
|-- evaluation_dataset.py
|-- evaluate_retreival.py
|-- test_chunker.py
|
|-- app/
|-- data/
|   |-- sample_documents/
|
|-- database/
|   |-- chroma_db/
|
|-- tests/
|
|-- requirements.txt
|-- .gitignore
|-- README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Enterprise_RAG_Assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Install Ollama

Download Ollama from:

https://ollama.com/download

### 6. Download the language model

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before using the application.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Open the Knowledge Base section.
2. Upload one or more PDF documents.
3. Select Process Documents.
4. Wait for document extraction, chunking, embedding, and indexing to finish.
5. Open Knowledge Search.
6. Enter a question about the uploaded documents.
7. Review the generated answer and its document source references.

## Evaluation

The project includes a small custom retrieval evaluation dataset containing four questions.

The evaluation checks whether expected keywords are present in the retrieved document chunks.

A previous test achieved 4 out of 4 keyword checks (100% keyword coverage).

This result represents only the custom test dataset. It does not establish overall RAG accuracy, answer faithfulness, or production reliability.

## Current Limitations

- Currently supports PDF documents.
- Uses a locally configured language model.
- Retrieval quality depends on document structure and chunking.
- Evidence extraction and retrieval ranking can be improved.
- Advanced evaluation metrics are not yet implemented.
- Authentication, multi-user access control, and production security are not implemented.

## Future Improvements

- Support additional document formats.
- Improve document-aware chunking.
- Improve retrieval ranking and evidence extraction.
- Implement retrieval precision and recall.
- Evaluate answer faithfulness and relevance.
- Add citation coverage evaluation.
- Introduce user authentication and access controls.
- Develop API integration.
- Deploy the application in a secure environment.

## Project Purpose

This project was developed to gain practical experience with Retrieval-Augmented Generation, semantic search, vector databases, embeddings, and local Large Language Models.

It demonstrates a foundational implementation of an AI-powered document assistant.

## Author

Susarla Vishnuvardhan

B.Tech Computer Science and Engineering - Artificial Intelligence (2026)

GitHub: https://github.com/susalavishnuvardhan227-art

---

**Note:** This is an educational portfolio prototype and is not intended to be used as a production enterprise system without further security, evaluation, and reliability improvements.