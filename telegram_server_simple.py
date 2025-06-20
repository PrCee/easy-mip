from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import logging
from telegram_handler_simple import TelegramHandlerSimple
from config import TELEGRAM_TOKEN

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(title="MIP Generator Telegram Bot", version="1.0.0")

# Verificar se o token está configurado
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não configurado. Configure a variável de ambiente TELEGRAM_TOKEN.")

# Inicializar handler do Telegram
telegram_handler = TelegramHandlerSimple(TELEGRAM_TOKEN)

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
    print("🤖 Iniciando MIP Generator Telegram Bot (Versão Simplificada)...")
    print(f"📱 Bot Token: {TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else 'NÃO CONFIGURADO'}...")
    print("🌐 Servidor rodando em: http://localhost:8000")
    print("📋 Endpoints disponíveis:")
    print("  - GET  / - Status do servidor")
    print("  - POST /webhook/telegram - Webhook do Telegram")
    print("  - GET  /bot-info - Informações do bot")
    print("\n💡 Para desenvolvimento local, use ngrok:")
    print("   ngrok http 8000")
    print("   Depois configure o webhook com a URL do ngrok")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 