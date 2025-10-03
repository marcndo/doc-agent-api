# api/main.py
from fastapi import FastAPI
import uvicorn

# Create a FastAPI app instance
app = FastAPI(title="Smart Document Q&A API")

@app.get("/")
def read_root():
    """A simple endpoint to test if the API is running."""
    return {"status": "ok", "message": "Welcome to the Document Q&A API!"}

# This part allows running the script directly for development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)