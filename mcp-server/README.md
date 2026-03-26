# MCP Server - Open Intelligence IA

Servidor MCP que expõe as skills OSINT para Agentes IA (Claude, Gemini, etc.).
Ele consulta o [backend FastAPI](../backend) e traduz os resultados em ferramentas compreensíveis pela IA.

## Instalação

```bash
cd mcp-server
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Skills Disponíveis

| Tool | Descrição |
|------|-----------|
| `search_personal_memory` | Busca semântica em tudo que o usuário já leu na web |
| `cross_reference_entity` | Dossiê de uma entidade (pessoa, empresa, IP) no histórico |

## Conectando ao Claude Desktop

Edite o arquivo `~/snap/claude-desktop/current/.config/claude/claude_desktop_config.json`
(ou o caminho equivalente para seu OS) e adicione:

```json
{
  "mcpServers": {
    "open-intelligence": {
      "command": "/home/bonafe/git/open-inteligence-ia/mcp-server/.venv/bin/python",
      "args": ["/home/bonafe/git/open-inteligence-ia/mcp-server/server.py"]
    }
  }
}
```

> ⚠️ O backend (`uvicorn main:app --port 8000`) deve estar rodando antes de usar o MCP.
