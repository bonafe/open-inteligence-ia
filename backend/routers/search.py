"""
Router de Busca Semântica.
Recebe uma query em linguagem natural e retorna os chunks mais relevantes do histórico.
"""
from fastapi import APIRouter, Query
from services.embedder import get_embeddings
from services.vector_store import query_documents

router = APIRouter()


@router.get("/search")
def search(q: str = Query(..., description="Query em linguagem natural"), limit: int = Query(5, ge=1, le=20)):
    """
    Busca semântica na memória de navegação.
    Retorna os trechos de páginas más similares à query, com URL e título de origem.
    """
    query_embedding = get_embeddings([q])[0]
    results = query_documents(query_embedding=query_embedding, n_results=limit)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    hits = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        hits.append({
            "score": round(1 - dist, 4),  # Converte distância coseno em score de 0 a 1
            "url": meta.get("url"),
            "title": meta.get("title"),
            "timestamp": meta.get("timestamp"),
            "excerpt": doc
        })

    return {"query": q, "results": hits}
