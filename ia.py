import os
import requests

headers={
    "Content-Type": "application/json",
    "X-goog-api-key": os.getenv("GEMINI_API_KEY"),
},


def responder_com_ia(pergunta_cliente, catalogo_texto):
    """Usa o Gemini para responder o cliente com base no catálogo da loja."""

    prompt = f"""Você é um atendente virtual de uma loja que vende pelo Telegram.
Seja simpático, direto e breve (poucas frases).
Use o catálogo abaixo para responder dúvidas sobre produtos, preços e formas de compra.
Se o cliente quiser comprar, oriente a usar o comando /produtos para ver a lista com botões.
Se a pergunta não tiver relação com a loja, responda educadamente que só pode ajudar com assuntos da loja.

Catálogo atual:
{catalogo_texto}

Pergunta do cliente: {pergunta_cliente}
"""

import os
import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": os.getenv("GEMINI_API_KEY")
}

def responder_com_ia(pergunta_cliente, catalogo_texto):
    prompt = f"""Você é um atendente virtual de uma loja.
Seja simpático, direto e breve (poucas frases).
Use o catálogo abaixo para responder dúvidas sobre produtos.
Se o cliente quiser comprar, oriente a usar o comando /comprar.
Se a pergunta não tiver relação com a loja, responda de forma cortês.

Catálogo atual:
{catalogo_texto}

Pergunta do cliente: {pergunta_cliente}
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Erro Gemini API: {res_data}")
            return "Desculpe, ocorreu um erro ao processar sua resposta."
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return "Desculpe, serviço indisponível no momento."
