import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do MIP Generator Telegram Bot

# Token do bot do Telegram (deve ser configurado via variável de ambiente)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configurações do servidor
HOST = "0.0.0.0"
PORT = 8000

# Configurações de logging
LOG_LEVEL = "INFO"

# Configurações de arquivos
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

# Configurações do Whisper
WHISPER_MODEL = "base"

# Configurações de sessão
SESSION_TIMEOUT = 3600  # 1 hora em segundos 