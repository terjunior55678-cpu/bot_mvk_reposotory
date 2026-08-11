import os
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


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

    try:
        resp = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY,
            },
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 300,
                },
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Erro na IA: {e}")
        return (
            "Desculpa, tive um problema para responder agora. "
            "Tenta de novo em instantes ou use /produtos para ver o catálogo."
        )
