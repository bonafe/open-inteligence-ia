# Backend - Open Intelligence IA

Backend local em Python/FastAPI para ingestão e busca semântica da memória de navegação OSINT.

## Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando (modo local)

## Instalação

```bash
cd backend

# 1. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure o ambiente
cp .env.example .env
# Edite o .env se quiser usar OpenAI em vez do Ollama

# 4. (Modo Local) Baixe o modelo de embeddings do Ollama
ollama pull nomic-embed-text
```

## Rodando o servidor

```bash
uvicorn main:app --reload --port 8000
```

O servidor estará disponível em `http://localhost:8000`.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Health check do serviço |
| `POST` | `/ingest` | Recebe dados da Extensão do Chrome |
| `GET` | `/search?q=<query>` | Busca semântica na memória |

## Testando manualmente

```bash
# Health check
curl http://localhost:8000/health

# Busca semântica
curl "http://localhost:8000/search?q=vazamento+de+dados"
```
