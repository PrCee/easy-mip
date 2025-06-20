# 🤖 MIP Generator - Bot do Telegram

Gerador automatizado de Modelos de Instrução de Procedimento (MIPs) via Telegram Bot.

## 🚀 Funcionalidades

- **Bot do Telegram**: Interface intuitiva para criação de MIPs
- **Processamento de Áudio**: Transcrição automática com Whisper
- **Processamento de Imagens**: Download e organização de fotos
- **Geração de Documentos**: PDF, DOCX e HTML editáveis
- **Sessões Inteligentes**: Controle de estado por usuário

## 📋 Pré-requisitos

- Python 3.8+
- Bot do Telegram (token)
- ngrok (para desenvolvimento local)

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/mip-generator.git
cd mip-generator
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

### 🔐 Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Token do bot do Telegram (obrigatório)
TELEGRAM_TOKEN=seu_token_aqui

# Configurações do servidor
HOST=0.0.0.0
PORT=8000

# Configurações de logging
LOG_LEVEL=INFO
```

## 🤖 Configuração do Bot do Telegram

1. **Crie um bot no Telegram**
   - Acesse [@BotFather](https://t.me/BotFather)
   - Envie `/newbot`
   - Siga as instruções para criar o bot
   - Copie o token fornecido

2. **Configure o token**
   - Adicione o token ao arquivo `.env`
   - Exemplo: `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

## 🚀 Execução

### Desenvolvimento Local

1. **Inicie o servidor**
```bash
python telegram_server_simple.py
```

2. **Exponha o servidor com ngrok**
```bash
ngrok http 8000
```

3. **Configure o webhook**
```bash
python setup_webhook.py
```
- Escolha opção 1
- Cole a URL do ngrok + `/webhook/telegram`

### Produção

1. **Configure o webhook com sua URL de produção**
```bash
python setup_webhook.py
```

2. **Inicie o servidor**
```bash
python telegram_server_simple.py
```

## 📱 Como Usar

1. **Inicie o bot**: Envie `/start` para @RFTec_bot
2. **Crie um MIP**: Envie `/new`
3. **Envie o título**: Nome do procedimento
4. **Grave um áudio**: Descrição dos passos
5. **Envie as fotos**: Uma por passo
6. **Confirme**: Responda "sim" para gerar
7. **Receba os arquivos**: PDF, DOCX e HTML

## 🔧 Comandos Disponíveis

- `/start` - Iniciar o bot
- `/help` - Ver ajuda
- `/new` - Criar novo MIP
- `/status` - Ver status atual
- `/cancel` - Cancelar MIP atual

## 📁 Estrutura do Projeto

```
mip_generator/
├── telegram_server_simple.py    # Servidor principal
├── telegram_handler_simple.py   # Handler do bot
├── config.py                    # Configurações
├── setup_webhook.py            # Configurador de webhook
├── generate_*.py               # Geradores de MIP
├── requirements.txt            # Dependências
├── .env                        # Variáveis de ambiente (não commitado)
├── env.example                 # Exemplo de configuração
└── README.md                   # Este arquivo
```

## 🔒 Segurança

- ✅ Tokens removidos do código
- ✅ Variáveis de ambiente configuradas
- ✅ .gitignore configurado
- ✅ Arquivos sensíveis protegidos

## 🛠️ Desenvolvimento

### Estrutura de Sessões

```python
session = {
    "state": "initial|waiting_title|waiting_audio|waiting_images|waiting_confirmation",
    "title": "Título do procedimento",
    "audio_path": "caminho/para/audio.ogg",
    "images": ["caminho1.jpg", "caminho2.jpg"],
    "transcription": "Texto transcrito",
    "steps": ["Passo 1", "Passo 2"],
    "created_at": datetime.now()
}
```

### Estados do Bot

1. **initial**: Aguardando comando
2. **waiting_title**: Aguardando título
3. **waiting_audio**: Aguardando áudio
4. **waiting_images**: Aguardando fotos
5. **waiting_confirmation**: Aguardando confirmação

## 📞 Suporte

- **Telefone**: (11) 3090-0900
- **Email**: suporte@ramalvirtual.com.br
- **Website**: www.ramalvirtual.com.br

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ Importante

- **NUNCA** commite o arquivo `.env` com tokens reais
- **SEMPRE** use variáveis de ambiente para configurações sensíveis
- **TESTE** localmente antes de fazer deploy
- **MANTENHA** o ngrok atualizado para desenvolvimento