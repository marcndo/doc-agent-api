from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

print("Downloading the model ...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embeding model loaded successfully.")

def chunk_text(text:str) -> list[str]:
    """Splits a long text into smaller overlapping chunks

    Args:
        text (str): Long text to split

    Returns:
        list[str]: Overlapping chunks from Long text
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    print(f"Text split into {len(chunks)} chunks.")
    return chunks

def get_embeddings(text: list[str]) -> list(list[float]):
    """Convert chunked string to their numerical representation

    Args:
        chunks (list[str]): Chunked strings to be embedded
    """
    embedding = embedding_model.encode(text, show_progress_bar=True)
    print(f"Created {len(embedding)} embeddings.")
    return embedding

