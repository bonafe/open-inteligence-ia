"""
Serviço de Embeddings.
Suporta dois providers: 'ollama' (local, gratuito) e 'openai' (nuvem).
Configure via a variável EMBEDDING_PROVIDER no arquivo .env.
"""
import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nomic-embed-text")


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos."""
    if PROVIDER == "openai":
        return _embed_openai(texts)
    return _embed_ollama(texts)


def _embed_ollama(texts: list[str]) -> list[list[float]]:
    import ollama
    embeddings = []
    for text in texts:
        response = ollama.embeddings(model=OLLAMA_MODEL, prompt=text)
        embeddings.append(response["embedding"])
    return embeddings


def _embed_openai(texts: list[str]) -> list[list[float]]:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]
