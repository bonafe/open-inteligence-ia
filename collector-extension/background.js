/**
 * Script de Background da Extensão (Service Worker).
 * Fica rodando em segundo plano ouvindo as mensagens vindas das abas.
 */

const LOCAL_INGEST_API = "http://localhost:8000/ingest";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "page_captured") {
        console.log(`Recebido contexto da URL: ${message.data.url}`);
        
        // Disparamos o POST de forma assíncrona para o nosso backend Python local
        // que fará o Embedding e salvará no Banco Vetorial.
        fetch(LOCAL_INGEST_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message.data)
        })
        .then(response => {
            console.log("[Open Intelligence Collector] Dados enviados para o backend local com sucesso.");
        })
        .catch(err => {
            // Se o backend Python local nao estiver rodando, nao tem problema, 
            // a extensão falha silenciosamente sem atrapalhar o usuario.
            console.debug("Backend local não está ativo no momento.", err);
        });
    }
});
