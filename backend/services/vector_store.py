"""
Wrapper sobre o ChromaDB.
A coleção 'osint_memory' armazena todos os chunks de texto capturados da navegação.
"""
import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

# Cliente persistente: os dados sobrevivem ao reinício do servidor
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name="osint_memory",
    metadata={"hnsw:space": "cosine"}  # Melhor para similaridade semântica
)


def add_documents(ids: list[str], texts: list[str], embeddings: list[list[float]], metadatas: list[dict]):
    """Adiciona chunks ao banco vetorial."""
    _collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )


def query_documents(query_embedding: list[float], n_results: int = 5) -> dict:
    """Realiza busca por similaridade semântica."""
    return _collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
