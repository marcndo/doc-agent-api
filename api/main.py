from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

# Import our custom modules
from ingestion.processing import process_pdf, process_url
from embeddings.embedding import chunk_text, get_embeddings, create_faiss_index, load_faiss_index, embedding_model
from api.rag_handler import get_rag_response

app = FastAPI(title="Smart Document Q&A API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for the index and text chunks
faiss_index = None
text_chunks = []


# --- NEW: A single, more robust endpoint for processing ---
@app.post("/process/")
async def process_source(file: Optional[UploadFile] = File(None), url: Optional[str] = Form(None)):
    """
    Processes either an uploaded PDF file or a web URL to create a searchable index.
    """
    global faiss_index, text_chunks

    # 1. Validate Input: Ensure either a file or a URL is provided
    if file is None and url is None:
        raise HTTPException(status_code=400, detail="No source provided. Please upload a file or provide a URL.")
    if file and url:
        raise HTTPException(status_code=400, detail="Please provide either a file or a URL, not both.")

    full_text = ""
    source_name = ""

    try:
        # 2. Ingestion: Process the source based on its type
        if file:
            source_name = file.filename
            print(f"Processing uploaded file: {source_name}")
            content = await file.read()
            full_text = process_pdf(content)
        elif url:
            source_name = url
            print(f"Processing URL: {source_name}")
            full_text = process_url(url)

        if not full_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from the source.")

        # 3. Chunking
        print("Chunking text...")
        text_chunks = chunk_text(full_text)

        # 4. Embeddings & FAISS Index Creation
        print("Creating embeddings and FAISS index...")
        embeddings = get_embeddings(text_chunks)
        index_path = "temp_faiss_index.idx"
        create_faiss_index(embeddings, index_path)
        faiss_index = load_faiss_index(index_path)

        return {"status": "success",
                "message": f"Successfully processed '{source_name}' and created index with {len(text_chunks)} chunks."}

    except Exception as e:
        # Catch any other unexpected errors during processing
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/query/")
async def query(query_text: str = Form(...)):
    """
    Takes a user's query and returns a RAG-generated answer.
    """
    global faiss_index, text_chunks

    if faiss_index is None or not text_chunks:
        raise HTTPException(status_code=400, detail="Index not found. Please process a document or URL first.")

    try:
        answer = get_rag_response(query=query_text, index=faiss_index, chunks=text_chunks,
                                  embedding_model=embedding_model)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during query processing: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
