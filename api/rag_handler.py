import numpy as np
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_rag_response(query, index, chunks, embedding_model):
    """
    Generates a RAG response for a given query.

    Args:
        query: The user's question.
        index: The FAISS index of document chunks.
        chunks: The list of original text chunks.
        embedding_model: The sentence-transformer model for embeddings.

    Returns:
        The generated answer from the LLM.
    """
    if index is None:
        return "Error: Document index not found. Please upload a document first."

    # 1. Embed the user's query
    print(f"Embedding the query: '{query}'")
    query_embedding = embedding_model.encode([query])
    query_vector = np.array(query_embedding).astype('float32')

    # 2. Retrieve relevant context from FAISS
    # Search the index for the top k most similar chunks
    k = 3
    distances, indices = index.search(query_vector, k)

    # Get the actual text chunks using the indices
    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n\n---\n\n".join(retrieved_chunks)
    print(f"Retrieved {len(retrieved_chunks)} chunks of context.")

    # 3. Augment the prompt with the context
    template = """
    You are an intelligent assistant. Use the following context to answer the user's question.
    If you don't know the answer, just say that you don't know. Do not try to make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate.from_template(template)

    # 4. Generate the answer using the LLM
    print("Generating answer with the LLM...")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    # Create the RAG chain using LangChain Expression Language (LCEL)
    chain = prompt | llm | StrOutputParser()

    # Invoke the chain with the context and question
    answer = chain.invoke({"context": context, "question": query})

    return answer
