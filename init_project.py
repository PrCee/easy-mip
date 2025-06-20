#!/usr/bin/env python3
"""
Script de inicialização do MIP Generator
Configura o ambiente de forma segura
"""

import os
import shutil
from pathlib import Path

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Criando arquivo .env a partir do exemplo...")
            shutil.copy(env_example, env_file)
            print("✅ Arquivo .env criado!")
            print("⚠️  IMPORTANTE: Configure o TELEGRAM_TOKEN no arquivo .env")
        else:
            print("❌ Arquivo env.example não encontrado!")
            return False
    else:
        print("✅ Arquivo .env já existe")
    
    return True

def check_directories():
    """Cria diretórios necessários"""
    directories = ["uploads", "output", "assets"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório {directory}/ criado/verificado")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi
        import requests
        import uvicorn
        print("✅ Dependências principais instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def check_telegram_token():
    """Verifica se o token do Telegram está configurado"""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    if not token or token == "seu_token_aqui":
        print("❌ TELEGRAM_TOKEN não configurado!")
        print("💡 Configure o token no arquivo .env")
        return False
    else:
        print("✅ TELEGRAM_TOKEN configurado")
        return True

def main():
    """Função principal"""
    print("🚀 INICIALIZADOR DO MIP GENERATOR")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Verificar arquivo .env
    if not check_env_file():
        return
    
    # Criar diretórios
    check_directories()
    
    # Verificar token
    if not check_telegram_token():
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Configure o TELEGRAM_TOKEN no arquivo .env")
        print("2. Execute: python telegram_server_simple.py")
        print("3. Use ngrok para expor o servidor")
        print("4. Configure o webhook com: python setup_webhook.py")
        return
    
    print("\n🎉 PROJETO CONFIGURADO COM SUCESSO!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python telegram_server_simple.py")
    print("2. Use ngrok para expor o servidor: ngrok http 8000")
    print("3. Configure o webhook: python setup_webhook.py")
    print("4. Teste o bot no Telegram!")

if __name__ == "__main__":
    main() 