import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from pathlib import Path
import whisper
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from twilio.rest import Client
import json
import logging
from whatsapp_handler import WhatsAppHandler
from document_template import MIPDocTemplate

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI()

# Inicializar modelo Whisper
model = whisper.load_model("base")

# Inicializar WhatsApp handler
whatsapp = WhatsAppHandler()

# Criar diretórios necessários
Path("uploads").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

class MIPSession:
    def __init__(self):
        self.audio_transcription = ""
        self.images = []
        self.title = ""
        self.steps = []
        self.timestamp = datetime.now()

    def add_image(self, image_path):
        self.images.append(image_path)

    def set_transcription(self, text):
        self.audio_transcription = text
        self._process_transcription()

    def _process_transcription(self):
        """Processa a transcrição para extrair título e passos"""
        lines = self.audio_transcription.split('\n')
        if lines:
            self.title = lines[0].strip()
            self.steps = [line.strip() for line in lines[1:] if line.strip()]

class DocumentGenerator:
    def __init__(self, session: MIPSession):
        self.session = session

    def generate_pdf(self, output_path):
        doc = MIPDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        doc.creation_date = self.session.timestamp.strftime('%d/%m/%Y %H:%M')

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Elementos do documento
        elements = []
        
        # Título do MIP
        elements.append(Paragraph("MODELO DE INSTRUÇÃO DE PROCEDIMENTO (MIP)", title_style))
        elements.append(Spacer(1, 12))
        
        # Título do procedimento
        elements.append(Paragraph(self.session.title, title_style))
        elements.append(Spacer(1, 24))

        # Passos
        for i, step in enumerate(self.session.steps, 1):
            elements.append(Paragraph(f"{i}. {step}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Adicionar imagem se disponível
            if i <= len(self.session.images):
                img = Image(self.session.images[i-1], width=400, height=300)
                elements.append(img)
                elements.append(Spacer(1, 12))

        doc.build(elements)

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """Endpoint para receber mensagens do WhatsApp"""
    try:
        form_data = await request.form()
        
        # Extrair informações da mensagem
        from_number = form_data.get("From", "").replace("whatsapp:", "")
        message_body = form_data.get("Body", "")
        num_media = int(form_data.get("NumMedia", "0"))
        media_content_type = form_data.get("MediaContentType0", "")
        media_url = form_data.get("MediaUrl0", "")
        
        # Processar mensagem de texto
        if message_body and not num_media:
            whatsapp.handle_message(from_number, "text", message_text=message_body)
            return {"status": "success"}
        
        # Processar mídia
        if num_media > 0:
            if "audio" in media_content_type:
                # Processar áudio
                if whatsapp.handle_message(from_number, "audio", media_url):
                    session = whatsapp.sessions.get(from_number)
                    if session and session['audio_path']:
                        # Transcrever áudio
                        result = model.transcribe(session['audio_path'])
                        
                        # Criar ou atualizar sessão MIP
                        mip_session = MIPSession()
                        mip_session.set_transcription(result["text"])
                        
                        # Armazenar sessão MIP
                        session['mip_session'] = mip_session
                        
                        # Se estiver no modo batch e já tiver imagens
                        if session.get('mode') == 'batch' and session['images']:
                            # Gerar PDF
                            output_path = f"output/mip_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            doc_gen = DocumentGenerator(mip_session)
                            doc_gen.generate_pdf(output_path)
                            
                            # Enviar PDF
                            whatsapp.send_document(from_number, output_path)
                            whatsapp.send_message(
                                from_number,
                                "Documento MIP gerado com sucesso!"
                            )
                        else:
                            # Modo sequencial
                            whatsapp.send_message(
                                from_number,
                                "Áudio recebido e transcrito com sucesso! Envie as imagens correspondentes aos passos."
                            )
                
            elif "image" in media_content_type:
                # Processar imagem
                if whatsapp.handle_message(from_number, "image", media_url):
                    session = whatsapp.sessions.get(from_number)
                    if session:
                        # Se estiver no modo sequencial e tiver uma sessão MIP
                        if session.get('mode') == 'sequential' and 'mip_session' in session:
                            mip_session = session['mip_session']
                            mip_session.add_image(session['images'][-1])
                            
                            # Se número de imagens = número de passos, gerar PDF
                            if len(mip_session.images) == len(mip_session.steps):
                                # Gerar PDF
                                output_path = f"output/mip_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                                doc_gen = DocumentGenerator(mip_session)
                                doc_gen.generate_pdf(output_path)
                                
                                # Enviar PDF
                                whatsapp.send_document(from_number, output_path)
                                whatsapp.send_message(
                                    from_number,
                                    "Documento MIP gerado com sucesso!"
                                )
        
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """Endpoint para processar áudio"""
    # Implementar processamento de áudio
    pass

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """Endpoint para processar imagem"""
    # Implementar processamento de imagem
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 