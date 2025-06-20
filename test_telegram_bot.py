import requests
import json
from config import TELEGRAM_TOKEN

def test_bot_connection():
    """Testa a conexão com o bot do Telegram"""
    print("🤖 Testando conexão com o bot do Telegram...")
    
    # Testar se o bot está ativo
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            print("✅ Bot conectado com sucesso!")
            print(f"📱 Nome: {bot_info['result']['first_name']}")
            print(f"👤 Username: @{bot_info['result']['username']}")
            print(f"🆔 ID: {bot_info['result']['id']}")
            return True
        else:
            print(f"❌ Erro ao conectar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_webhook_info():
    """Testa informações do webhook"""
    print("\n🔗 Verificando webhook...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            webhook_info = response.json()
            print("✅ Webhook info obtida!")
            print(f"📡 URL: {webhook_info['result'].get('url', 'Não configurado')}")
            print(f"📊 Total de updates: {webhook_info['result'].get('pending_update_count', 0)}")
            return webhook_info['result']
        else:
            print(f"❌ Erro ao obter webhook info: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro ao verificar webhook: {e}")
        return None

def send_test_message(chat_id):
    """Envia mensagem de teste"""
    print(f"\n📤 Enviando mensagem de teste para {chat_id}...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": "🤖 Teste do MIP Generator Bot!\n\nBot está funcionando corretamente! ✅",
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao enviar mensagem: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO BOT TELEGRAM")
    print("=" * 50)
    
    # Testar conexão
    if not test_bot_connection():
        print("\n❌ Falha na conexão. Verifique o token.")
        return
    
    # Verificar webhook
    webhook_info = test_webhook_info()
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Inicie o servidor: python telegram_server.py")
    print("2. Use ngrok para expor o servidor:")
    print("   ngrok http 8000")
    print("3. Configure o webhook com a URL do ngrok:")
    print("   https://api.telegram.org/bot[TOKEN]/setWebhook?url=https://[SEU-NGROK].ngrok.io/webhook/telegram")
    print("4. Teste o bot enviando /start")
    
    # Perguntar se quer enviar mensagem de teste
    try:
        chat_id = input("\n💬 Digite seu Chat ID para enviar mensagem de teste (ou Enter para pular): ")
        if chat_id.strip():
            send_test_message(int(chat_id))
    except ValueError:
        print("❌ Chat ID inválido")
    except KeyboardInterrupt:
        print("\n👋 Teste cancelado")

if __name__ == "__main__":
    main() 