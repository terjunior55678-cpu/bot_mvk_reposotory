import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de logs para monitoramento no Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token do Telegram pego da variável de ambiente no Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Função do menu principal
def menu_principal():
    keyboard = [
        [InlineKeyboardButton("📦 Ver Produtos / Catálogo", callback_data="catalogo")],
        [InlineKeyboardButton("💳 Formas de Pagamento", callback_data="pagamento")],
        [InlineKeyboardButton("🛍️ Como Fazer um Pedido", callback_data="comprar")],
        [InlineKeyboardButton("💬 Falar com Atendente", callback_data="suporte")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = (
        "👋 *Seja bem-vindo ao nosso atendimento virtual!*\n\n"
        "Selecione uma das opções abaixo para que eu possa te ajudar:"
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown", reply_markup=menu_principal())

# Manipulador das escolhas nos botões
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # 1. Catálogo de Produtos
    if query.data == "catalogo":
        texto = (
            "📋 *NOSSO CATÁLOGO DE PRODUTOS*\n\n"
            "🔹 *Produto 1* - R$ 50,00\n"
            "_Descrição breve do produto 1_\n\n"
            "🔹 *Produto 2* - R$ 80,00\n"
            "_Descrição breve do produto 2_\n\n"
            "🔹 *Produto 3* - R$ 120,00\n"
            "_Descrição breve do produto 3_\n\n"
            "💡 Para fazer o pedido de qualquer item, escolha a opção *Como Fazer um Pedido* no menu."
        )
        keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="menu")]]
        await query.edit_message_text(text=texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # 2. Formas de Pagamento
    elif query.data == "pagamento":
        texto = (
            "💳 *FORMAS DE PAGAMENTO ACEITAS*\n\n"
            "✅ *Pix* (Aprovação imediata)\n"
            "✅ *Cartão de Crédito / Débito*\n"
            "✅ *Boleto Bancário*\n\n"
            "📌 Envie o comprovante após a transferência para validar o pedido."
        )
        keyboard = [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="menu")]]
        await query.edit_message_text(text=texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # 3. Como Comprar
    elif query.data == "comprar":
        texto = (
            "🛍️ *COMO REALIZAR SEU PEDIDO*\n\n"
            "1. Escolha os itens desejados no catálogo.\n"
            "2. Clique no botão abaixo para ir direto para o nosso atendimento humano.\n"
            "3. Envie a lista dos produtos e seu endereço de entrega!"
        )
        keyboard = [
            [InlineKeyboardButton("💬 Chamar no WhatsApp", url="https://wa.me/5500000000000")],
            [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="menu")]
        ]
        await query.edit_message_text(text=texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # 4. Atendimento Humano
    elif query.data == "suporte":
        texto = (
            "📞 *ATENDIMENTO AO CLIENTE*\n\n"
            "⏰ *Horário de Atendimento:*\n"
            "Segunda a Sexta: 08:00h às 18:00h\n"
            "Sábado: 08:00h às 12:00h\n\n"
            "Clique abaixo para falar direto com o nosso suporte:"
        )
        keyboard = [
            [InlineKeyboardButton("💬 Falar com Suporte no WhatsApp", url="https://wa.me/5500000000000")],
            [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="menu")]
        ]
        await query.edit_message_text(text=texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    # 5. Voltar ao Menu Principal
    elif query.data == "menu":
        mensagem = "Selecione uma das opções abaixo para que eu possa te ajudar:"
        await query.edit_message_text(text=mensagem, reply_markup=menu_principal())

def main():
    if not TELEGRAM_TOKEN:
        print("ERRO: TELEGRAM_TOKEN não configurado nas variáveis de ambiente.")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot sem IA rodando perfeitamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
