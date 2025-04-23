# Gerador Automatizado de MIP via WhatsApp

Sistema para geração automatizada de documentos MIP (Modelo de Instrução de Procedimento) a partir de áudios e imagens enviados via WhatsApp. O sistema suporta tanto prints de tela quanto fotos tiradas pelo celular.

## 🚀 Funcionalidades

- Recebimento de áudios e imagens via WhatsApp
- Suporte a prints de tela e fotos do celular
- Processamento e otimização automática de imagens
- Transcrição automática de áudio usando Whisper
- Processamento e organização do conteúdo em formato MIP
- Geração de PDF com formatação padronizada
- Envio do documento final via WhatsApp

## 📋 Modos de Operação

### 1. Modo Sequencial (Padrão)
1. Analista envia o áudio com as instruções
2. Sistema transcreve e identifica os passos
3. Sistema solicita as imagens na ordem
4. Analista envia cada imagem correspondente a cada passo
5. Sistema gera o PDF quando receber todas as imagens

### 2. Modo Batch
1. Analista envia "iniciar batch" para começar
2. Sistema entra no modo batch
3. Analista envia todas as imagens na ordem correta
4. Analista envia "pronto" quando terminar
5. Analista envia o áudio explicando o passo a passo
6. Sistema gera o PDF automaticamente

## 🖼️ Suporte a Imagens

### Formatos Suportados
- JPG/JPEG
- PNG
- HEIC/HEIF (formato comum em iPhones)

### Processamento Automático

#### Screenshots (Prints de Tela)
- Detecção automática de prints
- Ajuste de contraste e nitidez para melhor legibilidade
- Otimização de tamanho mantendo qualidade

#### Fotos do Celular
- Correção automática de orientação (EXIF)
- Redimensionamento proporcional
- Otimização para visualização no documento

#### Otimizações Gerais
- Redimensionamento inteligente (máx. 1200x800 pixels)
- Compressão otimizada (85% qualidade)
- Conversão para formato uniforme (JPEG)
- Remoção de transparência em PNGs

## ⚙️ Requisitos

- Python 3.8 ou superior
- Conta no Twilio com WhatsApp habilitado
- FFmpeg (para processamento de áudio)
- Pillow (para processamento de imagens)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/[seu-usuario]/mip-generator.git
cd mip-generator
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com:
```env
# Configurações do Twilio
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_PHONE_NUMBER=seu_numero_whatsapp

# Configurações do OpenAI (caso necessário para versão em nuvem do Whisper)
OPENAI_API_KEY=sua_chave_api

# Configurações do sistema
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=output
SESSION_TIMEOUT=120
```

4. Crie as pastas necessárias:
```bash
mkdir uploads output assets
```

5. Adicione seu logo:
- Coloque o arquivo do logo da empresa em `assets/logo.png`

## 🚀 Uso

1. Inicie o servidor:
```bash
python main.py
```

2. Configure o webhook do Twilio:
```
[SEU_DOMINIO]/webhook/whatsapp
```

3. Envie mensagens para o número do WhatsApp configurado:
   - Escolha o modo (sequencial ou batch)
   - Envie as imagens (prints ou fotos)
   - Envie o áudio com as instruções
   - Receba o documento MIP em PDF

## 📁 Estrutura do Projeto

```
mip-generator/
├── main.py                 # Arquivo principal com API FastAPI
├── whatsapp_handler.py     # Gerenciamento do WhatsApp
├── image_processor.py      # Processamento de imagens
├── document_template.py    # Template do documento
├── requirements.txt        # Dependências
├── .env                    # Configurações
├── assets/                 # Recursos (logo, etc)
├── uploads/               # Arquivos temporários
└── output/                # Documentos gerados
```

## ⚠️ Limitações Atuais

- Não suporta edição interativa de documentos
- Sessão expira após 2 minutos de inatividade
- Imagens são associadas aos passos na ordem de envio
- Necessário enviar imagens na ordem correta no modo batch

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do projeto: [https://github.com/seu-usuario/mip-generator](https://github.com/seu-usuario/mip-generator) 