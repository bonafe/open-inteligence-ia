"""
Servidor MCP para Open Intelligence IA.
Usa FastMCP para compatibilidade com `mcp dev`, Claude Desktop e outros clientes.

Para rodar com o inspector visual:
    mcp dev server.py

Para conectar via stdio (Claude Desktop, Cursor):
    python server.py
"""
import httpx
from mcp.server.fastmcp import FastMCP

BACKEND_URL = "http://localhost:8000"

mcp = FastMCP("Open Intelligence IA")


@mcp.tool()
async def search_personal_memory(query: str, limit: int = 5) -> str:
    """
    Busca na memória de navegação pessoal do usuário (tudo que ele já leu na web).
    Use quando o usuário perguntar sobre algo que pode ter visto recentemente:
    pessoas, empresas, eventos, fatos em páginas visitadas.
    Retorna trechos relevantes com URLs e timestamps.

    Args:
        query: Consulta em linguagem natural, ex: 'CEO empresa de segurança vazamento'
        limit: Número máximo de resultados (padrão 5, máximo 20)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BACKEND_URL}/search", params={"q": query, "limit": limit})
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])
    if not results:
        return f"Nenhuma memória encontrada para: '{query}'."

    lines = [f"🔍 Busca: '{query}' — {len(results)} resultado(s)\n"]
    for i, hit in enumerate(results, 1):
        lines.append(
            f"[{i}] Score: {hit['score']:.2f}\n"
            f"    📰 {hit['title']}\n"
            f"    🔗 {hit['url']}\n"
            f"    🕐 {hit['timestamp']}\n"
            f"    📄 ...{hit['excerpt'][:300]}...\n"
        )
    return "\n".join(lines)


@mcp.tool()
async def cross_reference_entity(entity_name: str, limit: int = 10) -> str:
    """
    Faz um dossiê de uma entidade (pessoa, empresa, domínio ou IP) buscando
    TODAS as menções a ela no histórico de navegação do usuário.
    Use para investigações OSINT sobre um alvo específico.

    Args:
        entity_name: Nome da entidade, ex: 'Empresa XYZ', 'João Silva', '192.168.1.1'
        limit: Número máximo de menções (padrão 10)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BACKEND_URL}/search", params={"q": entity_name, "limit": limit})
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])
    if not results:
        return f"Nenhuma menção à entidade '{entity_name}' encontrada no histórico."

    # Agrupa por URL para montar o dossiê
    seen_urls: dict = {}
    for hit in results:
        if hit["url"] not in seen_urls:
            seen_urls[hit["url"]] = hit

    lines = [f"🕵️ Dossiê OSINT: '{entity_name}'\n", f"Encontrado em {len(seen_urls)} fonte(s):\n"]
    for i, (url, hit) in enumerate(seen_urls.items(), 1):
        lines.append(
            f"[Fonte {i}]\n"
            f"  📰 {hit['title']}\n"
            f"  🔗 {url}\n"
            f"  🕐 {hit['timestamp']}\n"
            f"  📄 ...{hit['excerpt'][:400]}...\n"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
