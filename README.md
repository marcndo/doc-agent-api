# Smart Document Processing & Q&A API (RAG-based)

## Overview:

Developed an end-to-end document intelligence system that allows users to upload PDFs, CSVs, and web links for automatic processing, storage, and retrieval. The system uses embeddings, vector databases, and LLM-powered retrieval-augmented generation (RAG) to enable natural language question answering over uploaded content.

## Key Features:

* Multi-format Ingestion: Parses PDFs, CSVs, and web pages into clean text for downstream processing.
* Embeddings & Vector Database: Converts text into dense embeddings using Hugging Face sentence-transformers and stores them in FAISS/ChromaDB for fast similarity search.
* RAG Pipeline: Implements retrieval-augmented generation, combining semantic search with an LLM (Falcon, Mistral, or OpenAI API) to provide accurate, context-aware answers.
* FastAPI Backend: Exposes REST endpoints (/upload, /query) for easy integration with external apps.
* Streamlit Frontend: Simple UI for document upload and interactive chat.
* Deployment: Containerized with Docker and deployed on AWS EC2, making it production-ready.
* Monitoring & Logging: Includes logging of user queries, latency, and error handling for reliability.
  
## Tech Stack:
* Languages/Frameworks: Python, FastAPI, Streamlit
* AI/ML: Hugging Face Transformers, Sentence-Transformers, LangChain
* Database: FAISS/ChromaDB (Vector DB)
* DevOps: Docker, AWS EC2
* Others: Git, Postman (API testing), Logging/Monitoring tools

## Impact / Value:
* Demonstrates the ability to design and implement real-world AI systems, from data ingestion to deployment.
* Showcases AI engineering + ML engineering skills: API development, RAG pipelines, system design, and cloud deployment.
* Recruiter-friendly: proves ability to work with LLMs, embeddings, MLOps, and full-stack integration.
