import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
import whisper
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramHandler:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.sessions: Dict[int, Dict] = {}  # chat_id -> session_data
        
        # Criar diretórios necessários
        Path("uploads").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)
        
        # Carregar modelo Whisper
        self.whisper_model = whisper.load_model("base")
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = "HTML") -> bool:
        """Envia mensagem de texto para o chat"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            response = requests.post(url, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False
    
    def send_document(self, chat_id: int, file_path: str, caption: str = "") -> bool:
        """Envia documento para o chat"""
        try:
            url = f"{self.base_url}/sendDocument"
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {
                    "chat_id": chat_id,
                    "caption": caption
                }
                response = requests.post(url, data=data, files=files)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao enviar documento: {e}")
            return False
    
    def download_file(self, file_id: str, file_path: str) -> bool:
        """Baixa arquivo do Telegram"""
        try:
            # Obter informações do arquivo
            url = f"{self.base_url}/getFile"
            data = {"file_id": file_id}
            response = requests.post(url, json=data)
            
            if response.status_code != 200:
                return False
            
            file_info = response.json()["result"]
            file_url = f"https://api.telegram.org/file/bot{self.token}/{file_info['file_path']}"
            
            # Baixar arquivo
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
                return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo: {e}")
            return False
    
    def get_session(self, chat_id: int) -> Dict:
        """Obtém ou cria sessão para o chat"""
        if chat_id not in self.sessions:
            self.sessions[chat_id] = {
                "state": "initial",
                "audio_path": None,
                "images": [],
                "transcription": "",
                "title": "",
                "steps": [],
                "created_at": datetime.now()
            }
        return self.sessions[chat_id]
    
    def handle_message(self, update: Dict) -> str:
        """Processa mensagem recebida do Telegram"""
        try:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            
            if not chat_id:
                return "Erro: Chat ID não encontrado"
            
            session = self.get_session(chat_id)
            
            # Comandos de texto
            if text:
                return self.handle_text_message(chat_id, text, session)
            
            # Mídia (áudio, imagem, documento)
            if "audio" in message:
                return self.handle_audio_message(chat_id, message["audio"], session)
            elif "voice" in message:
                return self.handle_voice_message(chat_id, message["voice"], session)
            elif "photo" in message:
                return self.handle_photo_message(chat_id, message["photo"], session)
            elif "document" in message:
                return self.handle_document_message(chat_id, message["document"], session)
            
            return "Tipo de mensagem não suportado"
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return f"Erro interno: {str(e)}"
    
    def handle_text_message(self, chat_id: int, text: str, session: Dict) -> str:
        """Processa mensagem de texto"""
        text = text.strip()
        
        if text.startswith("/"):
            return self.handle_command(chat_id, text, session)
        
        # Se estiver aguardando título
        if session["state"] == "waiting_title":
            session["title"] = text
            session["state"] = "waiting_audio"
            return ("✅ Título definido! Agora envie um áudio descrevendo os passos do procedimento.\n\n"
                   "💡 Dica: Fale de forma clara e pausada para melhor transcrição.")
        
        # Se estiver aguardando confirmação
        if session["state"] == "waiting_confirmation":
            if text.lower() in ["sim", "s", "yes", "y"]:
                return self.generate_mip(chat_id, session)
            elif text.lower() in ["não", "nao", "n", "no"]:
                session["state"] = "initial"
                return "❌ MIP cancelado. Use /new para começar novamente."
            else:
                return "Por favor, responda 'sim' ou 'não'."
        
        # Mensagem genérica
        return ("Olá! Sou o bot de geração de MIPs.\n\n"
               "Use /new para criar um novo MIP ou /help para ver todos os comandos.")
    
    def handle_command(self, chat_id: int, command: str, session: Dict) -> str:
        """Processa comandos do bot"""
        command = command.lower()
        
        if command == "/start":
            return ("🤖 <b>Bot MIP Generator</b>\n\n"
                   "Olá! Eu ajudo você a criar Modelos de Instrução de Procedimento (MIPs).\n\n"
                   "📋 <b>Como funciona:</b>\n"
                   "1. Envie o título do procedimento\n"
                   "2. Grave um áudio descrevendo os passos\n"
                   "3. Envie fotos de cada passo\n"
                   "4. Receba o MIP em PDF e DOCX\n\n"
                   "Use /new para começar!")
        
        elif command == "/help":
            return ("📚 <b>Comandos Disponíveis:</b>\n\n"
                   "/start - Iniciar o bot\n"
                   "/new - Criar novo MIP\n"
                   "/status - Ver status atual\n"
                   "/cancel - Cancelar MIP atual\n"
                   "/help - Esta ajuda\n\n"
                   "📞 <b>Suporte:</b> (11) 3090-0900")
        
        elif command == "/new":
            # Resetar sessão
            session.clear()
            session.update({
                "state": "waiting_title",
                "audio_path": None,
                "images": [],
                "transcription": "",
                "title": "",
                "steps": [],
                "created_at": datetime.now()
            })
            return ("🆕 <b>Novo MIP</b>\n\n"
                   "Primeiro, envie o título do procedimento.\n\n"
                   "Exemplo: 'Configuração de Impressora HP'")
        
        elif command == "/status":
            return self.get_status_message(session)
        
        elif command == "/cancel":
            session["state"] = "initial"
            return "❌ MIP cancelado. Use /new para começar novamente."
        
        else:
            return "❓ Comando não reconhecido. Use /help para ver os comandos disponíveis."
    
    def handle_audio_message(self, chat_id: int, audio: Dict, session: Dict) -> str:
        """Processa mensagem de áudio"""
        if session["state"] not in ["waiting_audio", "waiting_images"]:
            return "❌ Envie um áudio apenas quando solicitado. Use /new para começar."
        
        try:
            # Baixar áudio
            file_id = audio["file_id"]
            file_path = f"uploads/audio_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg"
            
            if not self.download_file(file_id, file_path):
                return "❌ Erro ao baixar áudio. Tente novamente."
            
            # Transcrever áudio
            self.send_message(chat_id, "🎵 Processando áudio...")
            result = self.whisper_model.transcribe(file_path)
            transcription = result["text"].strip()
            
            if not transcription:
                return "❌ Não foi possível transcrever o áudio. Tente falar mais claramente."
            
            # Processar transcrição
            session["audio_path"] = file_path
            session["transcription"] = transcription
            session["state"] = "waiting_images"
            
            # Extrair passos da transcrição
            lines = transcription.split('\n')
            session["steps"] = [line.strip() for line in lines if line.strip()]
            
            return (f"✅ <b>Áudio transcrito com sucesso!</b>\n\n"
                   f"📝 <b>Transcrição:</b>\n{transcription}\n\n"
                   f"📸 Agora envie as fotos dos passos (uma por vez).\n"
                   f"Você enviou {len(session['steps'])} passos, então envie {len(session['steps'])} fotos.")
        
        except Exception as e:
            logger.error(f"Erro ao processar áudio: {e}")
            return "❌ Erro ao processar áudio. Tente novamente."
    
    def handle_voice_message(self, chat_id: int, voice: Dict, session: Dict) -> str:
        """Processa mensagem de voz (trata como áudio)"""
        return self.handle_audio_message(chat_id, voice, session)
    
    def handle_photo_message(self, chat_id: int, photos: List[Dict], session: Dict) -> str:
        """Processa mensagem de foto"""
        if session["state"] != "waiting_images":
            return "❌ Envie fotos apenas quando solicitado. Use /new para começar."
        
        try:
            # Pegar a foto de maior resolução (última da lista)
            photo = photos[-1]
            file_id = photo["file_id"]
            file_path = f"uploads/image_{chat_id}_{len(session['images'])}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            
            if not self.download_file(file_id, file_path):
                return "❌ Erro ao baixar imagem. Tente novamente."
            
            session["images"].append(file_path)
            
            remaining = len(session["steps"]) - len(session["images"])
            
            if remaining > 0:
                return f"✅ Foto {len(session['images'])} recebida! Faltam {remaining} foto(s)."
            else:
                session["state"] = "waiting_confirmation"
                return (f"✅ <b>Todas as fotos recebidas!</b>\n\n"
                       f"📋 <b>Resumo do MIP:</b>\n"
                       f"• Título: {session['title']}\n"
                       f"• Passos: {len(session['steps'])}\n"
                       f"• Fotos: {len(session['images'])}\n\n"
                       f"Gerar MIP agora? (responda 'sim' ou 'não')")
        
        except Exception as e:
            logger.error(f"Erro ao processar foto: {e}")
            return "❌ Erro ao processar foto. Tente novamente."
    
    def handle_document_message(self, chat_id: int, document: Dict, session: Dict) -> str:
        """Processa mensagem de documento"""
        return "❌ Documentos não são suportados. Envie apenas fotos dos passos."
    
    def get_status_message(self, session: Dict) -> str:
        """Retorna mensagem de status da sessão"""
        if session["state"] == "initial":
            return "📊 <b>Status:</b> Nenhum MIP em andamento.\nUse /new para começar."
        
        status_text = f"📊 <b>Status do MIP:</b>\n"
        status_text += f"• Estado: {session['state']}\n"
        status_text += f"• Título: {session['title'] or 'Não definido'}\n"
        status_text += f"• Passos: {len(session['steps'])}\n"
        status_text += f"• Fotos: {len(session['images'])}\n"
        
        if session["transcription"]:
            status_text += f"• Transcrição: ✅\n"
        
        return status_text
    
    def generate_mip(self, chat_id: int, session: Dict) -> str:
        """Gera o MIP final"""
        try:
            self.send_message(chat_id, "🔄 Gerando MIP...")
            
            # Gerar arquivos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # PDF
            pdf_path = f"output/mip_{timestamp}.pdf"
            # TODO: Implementar geração com dados reais
            
            # DOCX
            docx_path = f"output/mip_{timestamp}.docx"
            # TODO: Implementar geração com dados reais
            
            # HTML
            html_path = f"output/mip_{timestamp}.html"
            # TODO: Implementar geração com dados reais
            
            # Enviar arquivos
            success_count = 0
            
            if os.path.exists(pdf_path):
                if self.send_document(chat_id, pdf_path, "📄 MIP em PDF"):
                    success_count += 1
            
            if os.path.exists(docx_path):
                if self.send_document(chat_id, docx_path, "📝 MIP editável (DOCX)"):
                    success_count += 1
            
            if os.path.exists(html_path):
                if self.send_document(chat_id, html_path, "🌐 MIP para Google Docs (HTML)"):
                    success_count += 1
            
            # Resetar sessão
            session["state"] = "initial"
            
            if success_count > 0:
                return f"✅ <b>MIP gerado com sucesso!</b>\n\n{success_count} arquivo(s) enviado(s).\n\nUse /new para criar outro MIP."
            else:
                return "❌ Erro ao gerar MIP. Tente novamente."
        
        except Exception as e:
            logger.error(f"Erro ao gerar MIP: {e}")
            return f"❌ Erro interno: {str(e)}" 