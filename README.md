# MIP Generator Bot

Gerador automatizado de documentos MIP (Modelo de Instrução de Procedimento) via Telegram.

## Funcionalidades

- Geração de MIPs a partir de:
  - Mensagens de texto
  - Mensagens de áudio (transcrição automática)
  - Imagens
- Formatação padronizada com:
  - Logo da empresa
  - Cabeçalho na primeira página
  - Rodapé na última página com QR code
- Interface amigável via bot do Telegram

## Requisitos

- Python 3.8+
- FFmpeg (para processamento de áudio)
- Conta no Telegram
- Bot do Telegram (token)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/PrCee/easy-mip.git
cd easy-mip
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as variáveis necessárias:
     - `TELEGRAM_TOKEN`: Token do seu bot do Telegram
     - `OPENAI_API_KEY`: (Opcional) Chave da API da OpenAI para transcrição de áudio
     - `UPLOAD_FOLDER`: Pasta para arquivos temporários
     - `OUTPUT_FOLDER`: Pasta para os PDFs gerados

4. Crie as pastas necessárias:
```bash
mkdir uploads output
```

## Criando um Bot no Telegram

1. Abra o Telegram e procure por "@BotFather"
2. Envie o comando `/newbot`
3. Siga as instruções para criar seu bot
4. Copie o token fornecido e adicione ao seu arquivo `.env`

## Uso

1. Inicie o bot:
```bash
python telegram_bot.py
```

2. No Telegram:
   - Procure pelo seu bot usando o nome que você definiu
   - Inicie uma conversa com `/start`
   - Use `/novo` para começar um novo MIP
   - Envie textos, áudios ou imagens
   - Use `/finalizar` quando terminar

## Comandos do Bot

- `/start` - Inicia a interação com o bot
- `/novo` - Começa um novo documento MIP
- `/ajuda` - Mostra a lista de comandos
- `/finalizar` - Gera o PDF do MIP
- `/cancelar` - Cancela o MIP atual

## Estrutura do Projeto

```
mip-generator/
├── assets/
│   └── logo.png
├── uploads/          # Arquivos temporários
├── output/           # PDFs gerados
├── document_template.py
├── telegram_bot.py
├── requirements.txt
└── .env
```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do projeto: [https://github.com/seu-usuario/mip-generator](https://github.com/seu-usuario/mip-generator)