from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest, search

app = FastAPI(
    title="Open Intelligence IA - Backend",
    description="API local para ingestão e busca semântica da memória de navegação OSINT.",
    version="1.0.0"
)

# Permite requisições da Extensão do Chrome (que tem origem `chrome-extension://...`)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(search.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Open Intelligence IA Backend"}
