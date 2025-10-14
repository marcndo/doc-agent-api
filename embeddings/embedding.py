import faiss
import numpy as np
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

print("Downloading the model ...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Download successful.")


def chunk_text(text):
    """Splits a long text into smaller overlapping chunks

    Args:
        text (str): Long text to split

    Returns:
        list[str]: Overlapping chunks from Long text
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(text)
    print(f"Text split into {len(text_chunks)} chunks.")
    return text_chunks


def get_embeddings(text):
    """Convert chunked string to their numerical representation

    Args:
        text (list[str]): Chunked strings to be embedded
    """
    embedding = embedding_model.encode(text, show_progress_bar=True)
    print("Created {len(embedding)} embeddings.")
    return embedding


def create_faiss_index(text_embeddings, index_path="faiss_index.idx"):
    """Create FAISS index from a list of embedding and save to a file

    Args:
        text_embeddings (list): List of embedding vectors
        index_path (str, optional): Path of here the index file was saved.
    """
    embeddings_np = np.array(text_embeddings).astype("float32")
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    faiss.write_index(index, index_path)
    print(f"FAISS index created with {index.ntotal} vectors and saved to {index_path}.")


def load_faiss_index(index_path="faiss_index.idx"):
    """
    Loads a FAISS index from a file.

    Args:
        index_path: The path to the index file.

    Returns:
        The loaded FAISS index object, or None if the file doesn't exist.
    """
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        print(f"FAISS index loaded from {index_path}. It contains {index.ntotal} vectors.")
        return index
    else:
        print("Index file not found at {index_path}.")
        return None





