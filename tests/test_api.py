from fastapi.testclient import TestClient
import sys
import os

# Add the root directory to the Python path to allow imports from api, ingestion, etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

# Create a TestClient instance
client = TestClient(app)


def test_process_no_source_provided():
    """
    Test Case 1: Ensure the API returns a 400 error if no file or URL is sent.
    This tests our input validation.
    """
    response = client.post("/process/")
    assert response.status_code == 400
    assert response.json() == {"detail": "No source provided. Please upload a file or provide a URL."}


def test_process_pdf_file():
    """
    Test Case 2: Test the 'happy path' for a successful PDF upload.
    This tests the file processing logic.
    """
    # Use the sample PDF from our test_data folder
    file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'sample.pdf')

    # Check if the sample file exists to avoid test errors
    if not os.path.exists(file_path):
        assert False, f"Test file not found at {file_path}. Please create a sample.pdf in the test_data directory."

    with open(file_path, "rb") as f:
        files = {"file": ("sample.pdf", f, "application/pdf")}
        response = client.post("/process/", files=files)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "Successfully processed 'sample.pdf'" in json_response["message"]


def test_end_to_end_url_and_query():
    """
    Test Case 3: Test the full end-to-end flow.
    1. Process a known URL.
    2. Ask a question related to that URL's content.
    This tests ingestion, chunking, embedding, indexing, and the RAG chain together.
    """
    # 1. Process a URL
    test_url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    response_process = client.post("/process/", data={"url": test_url})

    assert response_process.status_code == 200
    assert "Successfully processed" in response_process.json()["message"]

    # 2. Ask a question
    query = "What does RAG stand for?"
    response_query = client.post("/query/", data={"query_text": query})

    assert response_query.status_code == 200
    json_response = response_query.json()
    # Check if the answer contains relevant keywords, indicating the RAG process worked
    assert "answer" in json_response
    assert "retrieval-augmented generation" in json_response["answer"].lower()