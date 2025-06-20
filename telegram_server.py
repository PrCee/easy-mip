from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import logging
from telegram_handler import TelegramHandler
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(title="MIP Generator Telegram Bot", version="1.0.0")

# Inicializar handler do Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não configurado. Configure a variável de ambiente TELEGRAM_TOKEN.")

telegram_handler = TelegramHandler(TELEGRAM_TOKEN)

@app.get("/")
async def root():
    """Endpoint raiz para verificar se o servidor está funcionando"""
    return {
        "message": "MIP Generator Telegram Bot está funcionando!",
        "status": "online",
        "bot_username": "@RFTec_bot"
    }

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Endpoint para receber webhooks do Telegram"""
    try:
        # Obter dados da requisição
        update = await request.json()
        logger.info(f"Webhook recebido: {update}")
        
        # Processar mensagem
        response_text = telegram_handler.handle_message(update)
        
        # Enviar resposta
        if response_text:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            if chat_id:
                telegram_handler.send_message(chat_id, response_text)
        
        return JSONResponse(content={"status": "success"})
    
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/set-webhook")
async def set_webhook():
    """Configura o webhook do Telegram (para desenvolvimento)"""
    try:
        import requests
        
        # URL do webhook (substitua pela sua URL pública)
        webhook_url = "https://seu-dominio.com/webhook/telegram"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        data = {"url": webhook_url}
        
        response = requests.post(url, json=data)
        result = response.json()
        
        return {
            "status": "webhook_set",
            "result": result,
            "webhook_url": webhook_url
        }
    
    except Exception as e:
        logger.error(f"Erro ao configurar webhook: {e}")
        return {"error": str(e)}

@app.get("/get-webhook-info")
async def get_webhook_info():
    """Obtém informações do webhook atual"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
        response = requests.get(url)
        result = response.json()
        
        return result
    
    except Exception as e:
        logger.error(f"Erro ao obter webhook info: {e}")
        return {"error": str(e)}

@app.get("/delete-webhook")
async def delete_webhook():
    """Remove o webhook do Telegram"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
        response = requests.post(url)
        result = response.json()
        
        return {
            "status": "webhook_deleted",
            "result": result
        }
    
    except Exception as e:
        logger.error(f"Erro ao deletar webhook: {e}")
        return {"error": str(e)}

@app.get("/bot-info")
async def get_bot_info():
    """Obtém informações do bot"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
        response = requests.get(url)
        result = response.json()
        
        return result
    
    except Exception as e:
        logger.error(f"Erro ao obter bot info: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("🤖 Iniciando MIP Generator Telegram Bot...")
    print(f"📱 Bot Token: {TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else 'NÃO CONFIGURADO'}...")
    print("🌐 Servidor rodando em: http://localhost:8000")
    print("📋 Endpoints disponíveis:")
    print("  - GET  / - Status do servidor")
    print("  - POST /webhook/telegram - Webhook do Telegram")
    print("  - GET  /set-webhook - Configurar webhook")
    print("  - GET  /get-webhook-info - Informações do webhook")
    print("  - GET  /delete-webhook - Remover webhook")
    print("  - GET  /bot-info - Informações do bot")
    print("\n💡 Para desenvolvimento local, use ngrok:")
    print("   ngrok http 8000")
    print("   Depois configure o webhook com a URL do ngrok")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 