import os

def create_html_mip():
    """Cria um MIP em formato HTML que pode ser facilmente convertido"""
    
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIP - Procedimento de Configuração de Sistema</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #00517C;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #00517C;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 16px;
            font-weight: bold;
            color: #00517C;
            margin-bottom: 10px;
            border-bottom: 2px solid #00517C;
            padding-bottom: 5px;
        }
        .step {
            margin-bottom: 20px;
        }
        .step-title {
            font-size: 14px;
            font-weight: bold;
            color: #00517C;
            margin-bottom: 10px;
        }
        .bullet-list {
            margin-left: 20px;
        }
        .contact {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
        }
        .separator {
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="title">MODELO DE INSTRUÇÃO DE PROCEDIMENTO (MIP)</div>
    <div class="subtitle">Procedimento de Configuração de Sistema</div>
    
    <div class="separator"></div>
    
    <div class="section">
        <div class="section-title">VISÃO GERAL</div>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
    </div>
    
    <div class="section">
        <div class="section-title">ÍNDICE</div>
        <div class="bullet-list">
            <div>1. Preparação do Ambiente</div>
            <div>2. Configuração Inicial</div>
            <div>3. Teste do Sistema</div>
            <div>4. Validação Final</div>
        </div>
    </div>
    
    <div class="separator"></div>
    
    <div class="step">
        <div class="step-title">1. PREPARAÇÃO DO AMBIENTE</div>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        <div class="bullet-list">
            <div>• Verificar se todos os requisitos estão atendidos</div>
            <div>• Confirmar acesso ao sistema</div>
            <div>• Preparar credenciais de acesso</div>
        </div>
    </div>
    
    <div class="step">
        <div class="step-title">2. CONFIGURAÇÃO INICIAL</div>
        <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <div class="bullet-list">
            <div>• Acessar painel de configuração</div>
            <div>• Definir parâmetros básicos</div>
            <div>• Salvar configurações iniciais</div>
        </div>
    </div>
    
    <div class="step">
        <div class="step-title">3. TESTE DO SISTEMA</div>
        <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
        <div class="bullet-list">
            <div>• Executar testes automatizados</div>
            <div>• Verificar funcionalidades principais</div>
            <div>• Documentar resultados dos testes</div>
        </div>
    </div>
    
    <div class="step">
        <div class="step-title">4. VALIDAÇÃO FINAL</div>
        <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>
        <div class="bullet-list">
            <div>• Revisar todas as configurações</div>
            <div>• Confirmar funcionamento correto</div>
            <div>• Finalizar procedimento</div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">OBSERVAÇÕES IMPORTANTES</div>
        <div class="bullet-list">
            <div>• Semper in massa tempor nec feugiat nisl pretium fusce</div>
            <div>• Consectetur adipiscing elit duis tristique sollicitudin</div>
            <div>• In hac habitasse platea dictumst vestibulum rhoncus</div>
        </div>
    </div>
    
    <div class="contact">
        <div><strong>Suporte Ramal Virtual - (11) 3090-0900</strong></div>
        <div>suporte.ramalvirtual.com.br</div>
        <div>www.ramalvirtual.com.br    CEP:07021-050    Rua Santa Rita de Cássia 155</div>
    </div>
</body>
</html>"""
    
    # Salvar arquivo HTML
    output_path = "output/mip_google_docs_compatible.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"MIP em formato HTML gerado: {output_path}")
    print("\nPara usar no Google Docs:")
    print("1. Abra o arquivo HTML no navegador")
    print("2. Selecione todo o conteúdo (Ctrl+A)")
    print("3. Copie (Ctrl+C)")
    print("4. Cole no Google Docs (Ctrl+V)")
    print("5. A formatação será preservada!")

if __name__ == '__main__':
    # Criar diretório output se não existir
    os.makedirs("output", exist_ok=True)
    create_html_mip() 