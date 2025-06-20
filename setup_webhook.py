import requests
import json
from config import TELEGRAM_TOKEN

def setup_webhook(webhook_url):
    """Configura o webhook do Telegram"""
    print(f"🔗 Configurando webhook: {webhook_url}")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook configurado com sucesso!")
            print(f"📡 URL: {webhook_url}")
            return True
        else:
            print(f"❌ Erro ao configurar webhook: {result}")
            return False
    
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def get_webhook_info():
    """Obtém informações do webhook atual"""
    print("📊 Verificando webhook atual...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result["result"]
            print("✅ Informações do webhook:")
            print(f"📡 URL: {webhook_info.get('url', 'Não configurado')}")
            print(f"📊 Updates pendentes: {webhook_info.get('pending_update_count', 0)}")
            return webhook_info
        else:
            print(f"❌ Erro ao obter webhook info: {result}")
            return None
    
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def delete_webhook():
    """Remove o webhook do Telegram"""
    print("🗑️ Removendo webhook...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    
    try:
        response = requests.post(url)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook removido com sucesso!")
            return True
        else:
            print(f"❌ Erro ao remover webhook: {result}")
            return False
    
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_bot():
    """Testa se o bot está funcionando"""
    print("🤖 Testando bot...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get("ok"):
            bot_info = result["result"]
            print("✅ Bot funcionando!")
            print(f"📱 Nome: {bot_info['first_name']}")
            print(f"👤 Username: @{bot_info['username']}")
            print(f"🆔 ID: {bot_info['id']}")
            return True
        else:
            print(f"❌ Erro no bot: {result}")
            return False
    
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 CONFIGURADOR DE WEBHOOK")
    print("=" * 50)
    
    # Testar bot
    if not test_bot():
        print("\n❌ Bot não está funcionando. Verifique o token.")
        return
    
    # Verificar webhook atual
    webhook_info = get_webhook_info()
    
    print("\n📋 OPÇÕES:")
    print("1. Configurar webhook com URL personalizada")
    print("2. Remover webhook atual")
    print("3. Ver informações do webhook")
    print("4. Sair")
    
    while True:
        try:
            choice = input("\nEscolha uma opção (1-4): ").strip()
            
            if choice == "1":
                webhook_url = input("Digite a URL do webhook (ex: https://abc123.ngrok.io/webhook/telegram): ").strip()
                if webhook_url:
                    setup_webhook(webhook_url)
                else:
                    print("❌ URL inválida")
            
            elif choice == "2":
                delete_webhook()
            
            elif choice == "3":
                get_webhook_info()
            
            elif choice == "4":
                print("👋 Saindo...")
                break
            
            else:
                print("❌ Opção inválida")
        
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 