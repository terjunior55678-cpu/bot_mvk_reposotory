import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import init_db, listar_produtos, buscar_produto, criar_pedido
from ia import responder_com_ia

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))
RENDER_URL = os.environ.get("RENDER_URL")  # ex: https://seu-app.onrender.com


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! 👋 Bem-vindo(a) à nossa loja.\n\n"
        "Use /produtos para ver o catálogo\n"
        "Ou me pergunte qualquer coisa sobre nossos produtos!"
    )


async def produtos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    itens = listar_produtos()
    if not itens:
        await update.message.reply_text("Ainda não temos produtos cadastrados.")
        return

    botoes = [
        [InlineKeyboardButton(f"{p['nome']} - R$ {p['preco']:.2f}", callback_data=f"ver_{p['id']}")]
        for p in itens
    ]
    await update.message.reply_text(
        "🛍️ Nosso catálogo:", reply_markup=InlineKeyboardMarkup(botoes)
    )


async def ver_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    produto_id = int(query.data.split("_")[1])
    produto = buscar_produto(produto_id)

    if not produto:
        await query.edit_message_text("Produto não encontrado.")
        return

    criar_pedido(query.message.chat_id, produto_id)

    texto = (
        f"📦 *{produto['nome']}*\n\n"
        f"{produto['descricao'] or ''}\n\n"
        f"💰 R$ {produto['preco']:.2f}\n\n"
        f"Para comprar, clique no link abaixo:\n{produto['link_pagamento']}"
    )
    await query.edit_message_text(texto, parse_mode="Markdown")


async def mensagem_livre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Qualquer mensagem de texto que não seja comando vai pra IA responder."""
    itens = listar_produtos()
    catalogo_texto = "\n".join(
        f"- {p['nome']}: R$ {p['preco']:.2f} - {p['descricao'] or ''}" for p in itens
    ) or "Nenhum produto cadastrado ainda."

    resposta = responder_com_ia(update.message.text, catalogo_texto)
    await update.message.reply_text(resposta)


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("produtos", produtos))
    app.add_handler(CallbackQueryHandler(ver_produto, pattern=r"^ver_\d+$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_livre))

    if RENDER_URL:
        # Modo webhook (produção no Render)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"{RENDER_URL}/{BOT_TOKEN}",
        )
    else:
        # Modo polling (testes locais / Termux)
        app.run_polling()


if __name__ == "__main__":
    main()
