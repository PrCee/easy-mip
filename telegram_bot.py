import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
from pathlib import Path
from docx import Document
from docx.shared import Inches

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Diretórios para arquivos
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

class MIPGeneratorBot:
    def __init__(self):
        """Inicializa o bot do Telegram para geração de MIPs"""
        self.active_sessions = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Inicia a interação com o bot"""
        welcome_message = (
            "👋 Olá! Eu sou o bot gerador de MIPs.\n\n"
            "Posso ajudar você a criar documentos MIP a partir de:\n"
            "- 📝 Texto\n"
            "- 🎤 Áudio\n"
            "- 📸 Imagens\n\n"
            "Para começar, use um destes comandos:\n"
            "/novo - Iniciar um novo MIP\n"
            "/ajuda - Ver todas as opções disponíveis"
        )
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ajuda - Mostra a lista de comandos disponíveis"""
        help_message = (
            "📚 Comandos disponíveis:\n\n"
            "/novo - Iniciar um novo MIP\n"
            "/cancelar - Cancelar o MIP atual\n"
            "/status - Ver o status do MIP atual\n"
            "/ajuda - Mostrar esta mensagem\n\n"
            "Você também pode:\n"
            "- Enviar mensagens de texto\n"
            "- Enviar mensagens de áudio\n"
            "- Enviar imagens\n"
            "para adicionar conteúdo ao seu MIP."
        )
        await update.message.reply_text(help_message)

    async def new_mip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /novo - Inicia um novo documento MIP"""
        user_id = update.effective_user.id
        
        # Verifica se já existe uma sessão ativa
        if user_id in self.active_sessions:
            await update.message.reply_text(
                "❗ Você já tem um MIP em andamento.\n"
                "Use /cancelar para descartá-lo ou continue adicionando conteúdo."
            )
            return

        # Inicia nova sessão
        self.active_sessions[user_id] = {
            'content': [],
            'images': [],
            'title': None
        }

        await update.message.reply_text(
            "🆕 Vamos criar um novo MIP!\n\n"
            "Por favor, me diga qual será o título do MIP:"
        )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa mensagens de texto recebidas"""
        user_id = update.effective_user.id
        text = update.message.text

        if user_id not in self.active_sessions:
            await update.message.reply_text(
                "❗ Você ainda não iniciou um MIP.\n"
                "Use /novo para começar."
            )
            return

        session = self.active_sessions[user_id]
        
        # Se ainda não tem título, usa esta mensagem como título
        if not session['title']:
            session['title'] = text
            await update.message.reply_text(
                f"✅ Título definido: {text}\n\n"
                "Agora você pode:\n"
                "- Enviar mensagens de texto para o conteúdo\n"
                "- Enviar áudios que serão transcritos\n"
                "- Enviar imagens para incluir no documento\n\n"
                "Quando terminar, use /finalizar para gerar o PDF."
            )
            return

        # Adiciona o texto ao conteúdo
        session['content'].append(text)
        await update.message.reply_text("✅ Texto adicionado ao MIP!")

    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa mensagens de áudio recebidas"""
        await update.message.reply_text(
            "🎤 Recebi seu áudio!\n"
            "Em breve implementarei a transcrição usando Whisper."
        )

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa fotos recebidas"""
        user_id = update.effective_user.id
        
        if user_id not in self.active_sessions:
            await update.message.reply_text(
                "❗ Você ainda não iniciou um MIP.\n"
                "Use /novo para começar."
            )
            return

        # Pega a foto com maior resolução
        photo = update.message.photo[-1]
        
        # Baixa a foto
        file = await context.bot.get_file(photo.file_id)
        file_path = UPLOAD_FOLDER / f"photo_{len(self.active_sessions[user_id]['images'])}.jpg"
        await file.download_to_drive(file_path)
        
        # Adiciona o caminho da foto à sessão
        self.active_sessions[user_id]['images'].append(str(file_path))
        
        await update.message.reply_text(
            "📸 Imagem recebida e salva!\n"
            "Ela será incluída no documento final."
        )

    async def finalize(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /finalizar - Gera o PDF final"""
        user_id = update.effective_user.id
        
        if user_id not in self.active_sessions:
            await update.message.reply_text(
                "❗ Você ainda não iniciou um MIP.\n"
                "Use /novo para começar."
            )
            return

        session = self.active_sessions[user_id]
        
        if not session['content'] and not session['images']:
            await update.message.reply_text(
                "❗ Seu MIP está vazio!\n"
                "Adicione algum conteúdo antes de finalizar."
            )
            return

        await update.message.reply_text("🔄 Gerando seu PDF... Aguarde um momento.")

        try:
            # Gera o PDF
            output_path = OUTPUT_FOLDER / f"mip_{user_id}.pdf"
            doc = MIPDocTemplate(str(output_path), title=session['title'])
            story = []
            styles = getSampleStyleSheet()

            # Adiciona o conteúdo
            for text in session['content']:
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 12))

            # TODO: Adicionar imagens ao PDF

            # Muda para o template da última página
            story.append(NextPageTemplate('LastPage'))
            
            # Gera o documento
            doc.build(story)

            # Envia o PDF
            await update.message.reply_document(
                document=open(output_path, 'rb'),
                filename=f"MIP - {session['title']}.pdf"
            )

            # Limpa a sessão
            del self.active_sessions[user_id]

        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            await update.message.reply_text(
                "❌ Ocorreu um erro ao gerar o PDF.\n"
                "Por favor, tente novamente."
            )

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /cancelar - Cancela o MIP atual"""
        user_id = update.effective_user.id
        
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            await update.message.reply_text("❌ MIP cancelado!")
        else:
            await update.message.reply_text(
                "❗ Você não tem nenhum MIP em andamento."
            )

def main():
    """Função principal para iniciar o bot"""
    # Verifica se o token está configurado
    if not TELEGRAM_TOKEN:
        logger.error("Token do Telegram não encontrado! Configure TELEGRAM_TOKEN no arquivo .env")
        return

    # Cria o bot
    bot = MIPGeneratorBot()
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adiciona os handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("ajuda", bot.help))
    application.add_handler(CommandHandler("novo", bot.new_mip))
    application.add_handler(CommandHandler("finalizar", bot.finalize))
    application.add_handler(CommandHandler("cancelar", bot.cancel))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_text))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, bot.handle_audio))
    application.add_handler(MessageHandler(filters.PHOTO, bot.handle_photo))

    # Inicia o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
