/**
 * Script injetado em todas as paginas da web para capturar o contexto.
 * Ele eh executado silenciosamente assim que o documento termina de carregar.
 */

// Fazemos um clone do documento para não alterar a pagina atual caso modifiquemos o HTML
const clone = document.cloneNode(true);

// Removemos tags inuteis (scripts, css, iframes) para obter um texto limpo
const elementsToRemove = clone.querySelectorAll('script, style, nav, footer, iframe, noscript');
elementsToRemove.forEach(el => el.remove());

// Extraímos apenas o texto legível visível
const cleanText = clone.body ? clone.body.innerText : document.body.innerText;

// Empacotamos os metadados
const pageData = {
    url: window.location.href,
    title: document.title,
    content: cleanText.substring(0, 50000), // Limitamos o buffer para não enviar PDFs de texto infinito
    timestamp: new Date().toISOString()
};

// Enviamos os dados para o script background.js da extensão
chrome.runtime.sendMessage({
    action: "page_captured",
    data: pageData
});

console.log("[Open Intelligence Collector] Conteúdo capturado silenciosamente.");
