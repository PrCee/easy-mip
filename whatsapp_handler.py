from twilio.rest import Client
import os
from datetime import datetime, timedelta
import logging
from pathlib import Path
import requests
from pydub import AudioSegment
import json
from image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class WhatsAppHandler:
    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.sessions = {}
        self.session_timeout = int(os.getenv("SESSION_TIMEOUT", 120))
        self.image_processor = ImageProcessor()

    def _download_media(self, media_url, file_path):
        """Download mídia do WhatsApp"""
        response = requests.get(
            media_url,
            auth=(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )
        )
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
        return False

    def _convert_audio(self, input_path, output_path):
        """Converte áudio do WhatsApp para formato compatível com Whisper"""
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")

    def handle_message(self, from_number, message_type, media_url=None, message_text=None):
        """Processa mensagens recebidas do WhatsApp"""
        session = self._get_or_create_session(from_number)
        
        if message_type == "text":
            # Processar comandos de texto
            if message_text.lower() == "iniciar batch":
                session['mode'] = 'batch'
                session['status'] = 'waiting_images'
                self.send_message(
                    from_number,
                    "Modo batch ativado. Por favor, envie todas as imagens (prints ou fotos) na ordem correta dos passos. "
                    "Quando terminar, envie 'pronto' e depois o áudio com as instruções."
                )
                return True
            elif message_text.lower() == "pronto":
                if session.get('mode') == 'batch' and session.get('status') == 'waiting_images':
                    session['status'] = 'waiting_audio'
                    self.send_message(
                        from_number,
                        f"Recebi {len(session['images'])} imagens. Agora envie o áudio explicando o passo a passo."
                    )
                return True
            
        elif message_type == "audio":
            # Processar áudio
            audio_path = Path(f"uploads/audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg")
            if self._download_media(media_url, audio_path):
                wav_path = audio_path.with_suffix('.wav')
                self._convert_audio(audio_path, wav_path)
                session['audio_path'] = str(wav_path)
                
                # Se estiver no modo batch e esperando áudio
                if session.get('mode') == 'batch' and session.get('status') == 'waiting_audio':
                    return True
                else:
                    # Modo sequencial (padrão)
                    session['mode'] = 'sequential'
                    session['status'] = 'waiting_images'
                    return True
            
        elif message_type == "image":
            # Processar imagem
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            original_path = Path(f"uploads/original_image_{timestamp}.jpg")
            
            if self._download_media(media_url, original_path):
                # Processar e otimizar a imagem
                processed_path = Path(f"uploads/processed_image_{timestamp}.jpg")
                if self.image_processor.process_image(str(original_path), str(processed_path)):
                    session['images'].append(str(processed_path))
                    
                    # Remover imagem original após processamento
                    try:
                        original_path.unlink()
                    except:
                        pass
                    
                    # No modo batch, apenas confirma o recebimento
                    if session.get('mode') == 'batch' and session.get('status') == 'waiting_images':
                        self.send_message(
                            from_number,
                            f"Imagem {len(session['images'])} recebida e processada. Continue enviando as imagens ou envie 'pronto' quando terminar."
                        )
                        return True
                    
                    # No modo sequencial, verifica se completou todos os passos
                    elif session.get('mode') == 'sequential' and session.get('status') == 'waiting_images':
                        if 'mip_session' in session and len(session['images']) == len(session['mip_session'].steps):
                            return True
                        else:
                            self.send_message(
                                from_number,
                                "Imagem recebida e processada. Continue enviando as imagens na ordem dos passos."
                            )
                            return True
            
        return False

    def _get_or_create_session(self, from_number):
        """Gerencia sessões de usuário"""
        now = datetime.now()
        
        # Limpar sessões expiradas
        expired = [
            number for number, session in self.sessions.items()
            if (now - session['last_update']) > timedelta(seconds=self.session_timeout)
        ]
        for number in expired:
            del self.sessions[number]
        
        # Criar ou atualizar sessão
        if from_number not in self.sessions:
            self.sessions[from_number] = {
                'images': [],
                'audio_path': None,
                'last_update': now,
                'mode': None,  # 'batch' ou 'sequential'
                'status': None  # 'waiting_images', 'waiting_audio'
            }
        else:
            self.sessions[from_number]['last_update'] = now
            
        return self.sessions[from_number]

    def send_document(self, to_number, document_path):
        """Envia documento MIP gerado de volta para o usuário"""
        try:
            message = self.client.messages.create(
                from_=f"whatsapp:{os.getenv('TWILIO_PHONE_NUMBER')}",
                to=f"whatsapp:{to_number}",
                media_url=document_path
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar documento: {str(e)}")
            return False

    def send_message(self, to_number, message):
        """Envia mensagem de texto para o usuário"""
        try:
            self.client.messages.create(
                from_=f"whatsapp:{os.getenv('TWILIO_PHONE_NUMBER')}",
                to=f"whatsapp:{to_number}",
                body=message
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
            return False 