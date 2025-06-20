import os

def create_rtf_mip():
    """Cria um MIP em formato RTF (Rich Text Format) - altamente compatível"""
    
    rtf_content = r"""{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
\f0\fs24

{\qc\b\fs28 MODELO DE INSTRUÇÃO DE PROCEDIMENTO (MIP)\par}
{\qc\b\fs24 Procedimento de Configuração de Sistema\par}
\par

{\b\fs20 Visão Geral\par}
\fs20 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\par
\par

{\b\fs20 Índice\par}
\fs20 1. Preparação do Ambiente\par
2. Configuração Inicial\par
3. Teste do Sistema\par
4. Validação Final\par
\par

\page\par

{\b\fs20 1. Preparação do Ambiente\par}
\fs20 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\par
\par
• Verificar se todos os requisitos estão atendidos\par
• Confirmar acesso ao sistema\par
• Preparar credenciais de acesso\par
\par

{\b\fs20 2. Configuração Inicial\par}
\fs20 Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\par
\par
• Acessar painel de configuração\par
• Definir parâmetros básicos\par
• Salvar configurações iniciais\par
\par

{\b\fs20 3. Teste do Sistema\par}
\fs20 Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.\par
\par
• Executar testes automatizados\par
• Verificar funcionalidades principais\par
• Documentar resultados dos testes\par
\par

{\b\fs20 4. Validação Final\par}
\fs20 Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.\par
\par
• Revisar todas as configurações\par
• Confirmar funcionamento correto\par
• Finalizar procedimento\par
\par

{\b\fs20 Observações Importantes\par}
• Semper in massa tempor nec feugiat nisl pretium fusce\par
• Consectetur adipiscing elit duis tristique sollicitudin\par
• In hac habitasse platea dictumst vestibulum rhoncus\par
\par

{\qc\fs20 Suporte Ramal Virtual - (11) 3090-0900\par}
{\qc\fs20 suporte.ramalvirtual.com.br\par}
{\qc\fs20 www.ramalvirtual.com.br    CEP:07021-050    Rua Santa Rita de Cássia 155\par}
}"""
    
    # Salvar arquivo RTF
    output_path = "output/mip_google_docs_compatible.rtf"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rtf_content)
    
    print(f"MIP em formato RTF gerado: {output_path}")
    print("\nEste arquivo é altamente compatível com:")
    print("- Google Docs (upload direto)")
    print("- Microsoft Word Online")
    print("- Qualquer editor de texto")
    print("- Google Drive (abre automaticamente no Docs)")

if __name__ == '__main__':
    # Criar diretório output se não existir
    os.makedirs("output", exist_ok=True)
    create_rtf_mip() 