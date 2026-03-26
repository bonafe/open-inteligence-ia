"""
Router de Ingestão.
Recebe os dados da extensão do Chrome, divide em chunks, vetoriza e salva no ChromaDB.
"""
import hashlib
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.embedder import get_embeddings
from services.vector_store import add_documents

router = APIRouter()

# Divide o texto em chunks de ~500 chars com 50 chars de overlap para não perder contexto entre blocos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


class PagePayload(BaseModel):
    url: str
    title: str
    content: str
    timestamp: str


@router.post("/ingest", status_code=200)
def ingest_page(payload: PagePayload):
    """
    Endpoint chamado pela Extensão do Chrome sempre que o usuário visita uma nova página.
    """
    if not payload.content or len(payload.content.strip()) < 100:
        return {"status": "skipped", "reason": "Conteúdo da página muito curto para ser indexado."}

    # Divide o texto em partes menores para melhor granularidade na busca
    chunks = text_splitter.split_text(payload.content)

    if not chunks:
        return {"status": "skipped", "reason": "Nenhum chunk gerado."}

    # Gera um ID único por (URL + chunk_index) usando hash para evitar duplicatas
    ids = [
        hashlib.md5(f"{payload.url}::{i}".encode()).hexdigest()
        for i in range(len(chunks))
    ]

    # Metadados salvos junto com cada chunk para futura recuperação
    metadatas = [
        {
            "url": payload.url,
            "title": payload.title,
            "timestamp": payload.timestamp,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    try:
        embeddings = get_embeddings(chunks)
        add_documents(ids=ids, texts=chunks, embeddings=embeddings, metadatas=metadatas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar embeddings ou salvar: {str(e)}")

    return {
        "status": "ok",
        "url": payload.url,
        "chunks_indexed": len(chunks)
    }
