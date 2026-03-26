# Open Intelligence IA - Especificação de Arquitetura Inicial

## 1. Visão Geral
O objetivo deste projeto é criar um sistema que capture passivamente o contexto de navegação web do usuário, extraia entidades (nomes, fatos, organizações, notícias) e armazene essas informações em um banco de dados vetorial. Um Agente IA via **Model Context Protocol (MCP)** poderá então consultar esse banco para realizar conexões e fornecer inteligência (OSINT) baseada em todo o histórico de navegação.

## 2. Componentes da Arquitetura

Para que a experiência seja fluida e transparente, a arquitetura foi dividida em três pilares principais:

### Pilar 1: O Coletor (Collector)
Como capturar o texto sem atrapalhar a navegação diária?
* **Opção A (Recomendada): Extensão de Chrome**. Uma extensão simples que roda em background, captura o texto da página assim que ela termina de carregar e envia (junto com a URL e título) para o nosso backend local.
* **Opção B: Chrome DevTools Protocol (CDP)**. Um script Python/Node que se conecta na porta de debug do Chrome (`--remote-debugging-port=9222`). Exige iniciar o navegador com flags especiais. (Chromedriver puro é menos ideal pois exibe banners de "software de teste automático").
* **Decisão Inicial**: A definir com o usuário. A abordagem de Extensão costuma ter a melhor experiência para uso diário.

### Pilar 2: Backend e Processamento
Um servidor local leve (ex: Python com FastAPI local ou Node/Express) que recebe os dados do Coletor.
* **Limpeza**: Remove HTML, menús e dados inúteis.
* **Vetorização (Embeddings)**: Utiliza um modelo local (ex: Ollama) ou API (OpenAI) para transformar os textos e fatos em vetores (embeddings).
* **Armazenamento**: Salva os dados brutos e os vetores em um Banco de Dados Vetorial leve, como **ChromaDB**, **Qdrant** ou até **SQLite (com pgvector local)**.

### Pilar 3: O Servidor MCP e o Agente IA
O "cérebro" do OSINT.
* Será criado um **Servidor MCP** que expõe "Skills/Tools" para a IA.
* **Tools planejadas:**
  * `search_navigation_history(query)`: Busca semântica no banco vetorial pelas coisas que o usuário já viu.
  * `extract_entities(url)`: Pede para resumir ou cruzar dados de uma URL específica que está salva.
* Quando o usuário perguntar: *"Quem era aquele CEO da empresa de segurança que eu li sobre ontem e qual era a polêmica envolvendo ele?"*, a IA usará o MCP para buscar o vetor, entender o contexto e responder gerando inteligência cruzada.

## 3. Fluxo de Dados
1. Usuário acessa um artigo em `noticias.com`.
2. Extensão/Coletor extrai o texto do artigo -> Envia para `localhost:8000/ingest`.
3. Backend converte o texto para Embeddings -> Salva no `ChromaDB`.
4. Usuário abre a interface do Agente IA (Chat).
5. Usuário pergunta sobre o assunto.
6. Agente IA chama a tool (`MCP`) -> MCP consulta `ChromaDB` -> Agente cruza os fatos e responde.

## 4. Próximos Passos (Planejamento)
- [ ] Definir se usaremos Extensão ou Script CDP para o Coletor.
- [ ] Definir stack do Backend (ex: Python/FastAPI/ChromaDB).
- [ ] Definir o LLM (Ollama local ou APIs em Nuvem).
