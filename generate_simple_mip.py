import os

def create_simple_mip():
    """Cria um MIP em formato de texto simples que pode ser facilmente convertido"""
    
    content = """MODELO DE INSTRUÇÃO DE PROCEDIMENTO (MIP)

Procedimento de Configuração de Sistema

================================================================================

VISÃO GERAL

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu 
fugiat nulla pariatur.

================================================================================

ÍNDICE

1. Preparação do Ambiente
2. Configuração Inicial  
3. Teste do Sistema
4. Validação Final

================================================================================

1. PREPARAÇÃO DO AMBIENTE

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

• Verificar se todos os requisitos estão atendidos
• Confirmar acesso ao sistema
• Preparar credenciais de acesso

================================================================================

2. CONFIGURAÇÃO INICIAL

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu 
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in 
culpa qui officia deserunt mollit anim id est laborum.

• Acessar painel de configuração
• Definir parâmetros básicos
• Salvar configurações iniciais

================================================================================

3. TESTE DO SISTEMA

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore 
veritatis et quasi architecto beatae vitae dicta sunt explicabo.

• Executar testes automatizados
• Verificar funcionalidades principais
• Documentar resultados dos testes

================================================================================

4. VALIDAÇÃO FINAL

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, 
sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

• Revisar todas as configurações
• Confirmar funcionamento correto
• Finalizar procedimento

================================================================================

OBSERVAÇÕES IMPORTANTES

• Semper in massa tempor nec feugiat nisl pretium fusce
• Consectetur adipiscing elit duis tristique sollicitudin
• In hac habitasse platea dictumst vestibulum rhoncus

================================================================================

CONTATO

Suporte Ramal Virtual - (11) 3090-0900
suporte.ramalvirtual.com.br
www.ramalvirtual.com.br    CEP:07021-050    Rua Santa Rita de Cássia 155

================================================================================
"""
    
    # Salvar como arquivo de texto
    output_path = "output/mip_simple.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"MIP em formato texto gerado: {output_path}")
    print("\nPara usar no Google Docs:")
    print("1. Acesse docs.google.com")
    print("2. Crie um novo documento")
    print("3. Copie e cole o conteúdo do arquivo .txt")
    print("4. Formate conforme necessário")
    print("\nOu:")
    print("1. Faça upload do arquivo .txt no Google Drive")
    print("2. Clique com botão direito > 'Abrir com' > 'Google Docs'")

if __name__ == '__main__':
    # Criar diretório output se não existir
    os.makedirs("output", exist_ok=True)
    create_simple_mip() 