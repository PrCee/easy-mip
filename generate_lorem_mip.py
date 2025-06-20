from document_template import MIPDocTemplate
from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def generate_lorem_mip():
    """Gera um MIP de exemplo com lorem ipsum para demonstrar o formato"""
    
    # Criar o documento
    doc = MIPDocTemplate("output/lorem_mip_example.pdf", title="Procedimento de Exemplo")
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos customizados
    title_style = ParagraphStyle(
        'MIPTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centralizado
        textColor='#00517C'
    )
    
    subtitle_style = ParagraphStyle(
        'MIPSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor='#00517C'
    )
    
    step_style = ParagraphStyle(
        'MIPStep',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=15,
        leftIndent=20
    )
    
    # Título principal do MIP
    story.append(Paragraph("MODELO DE INSTRUÇÃO DE PROCEDIMENTO (MIP)", title_style))
    story.append(Spacer(1, 20))
    
    # Título do procedimento
    story.append(Paragraph("Procedimento de Configuração de Sistema", title_style))
    story.append(Spacer(1, 30))
    
    # Visão geral
    story.append(Paragraph("Visão Geral", subtitle_style))
    story.append(Paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        styles['Normal']
    ))
    story.append(Spacer(1, 20))
    
    # Índice
    story.append(Paragraph("Índice", subtitle_style))
    story.append(Paragraph("1. Preparação do Ambiente", step_style))
    story.append(Paragraph("2. Configuração Inicial", step_style))
    story.append(Paragraph("3. Teste do Sistema", step_style))
    story.append(Paragraph("4. Validação Final", step_style))
    story.append(Spacer(1, 30))
    
    # Mudar para template normal
    story.append(NextPageTemplate('Normal'))
    story.append(Spacer(1, 20))
    
    # Passo 1
    story.append(Paragraph("1. Preparação do Ambiente", subtitle_style))
    story.append(Paragraph(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        step_style
    ))
    story.append(Paragraph(
        "• Verificar se todos os requisitos estão atendidos<br/>"
        "• Confirmar acesso ao sistema<br/>"
        "• Preparar credenciais de acesso",
        step_style
    ))
    story.append(Spacer(1, 20))
    
    # Passo 2
    story.append(Paragraph("2. Configuração Inicial", subtitle_style))
    story.append(Paragraph(
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        step_style
    ))
    story.append(Paragraph(
        "• Acessar painel de configuração<br/>"
        "• Definir parâmetros básicos<br/>"
        "• Salvar configurações iniciais",
        step_style
    ))
    story.append(Spacer(1, 20))
    
    # Passo 3
    story.append(Paragraph("3. Teste do Sistema", subtitle_style))
    story.append(Paragraph(
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, "
        "totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
        step_style
    ))
    story.append(Paragraph(
        "• Executar testes automatizados<br/>"
        "• Verificar funcionalidades principais<br/>"
        "• Documentar resultados dos testes",
        step_style
    ))
    story.append(Spacer(1, 20))
    
    # Mudar para template da última página
    story.append(NextPageTemplate('LastPage'))
    story.append(Spacer(1, 20))
    
    # Passo 4
    story.append(Paragraph("4. Validação Final", subtitle_style))
    story.append(Paragraph(
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, "
        "sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
        step_style
    ))
    story.append(Paragraph(
        "• Revisar todas as configurações<br/>"
        "• Confirmar funcionamento correto<br/>"
        "• Finalizar procedimento",
        step_style
    ))
    story.append(Spacer(1, 30))
    
    # Observações finais
    story.append(Paragraph("Observações Importantes", subtitle_style))
    story.append(Paragraph(
        "• Semper in massa tempor nec feugiat nisl pretium fusce<br/>"
        "• Consectetur adipiscing elit duis tristique sollicitudin<br/>"
        "• In hac habitasse platea dictumst vestibulum rhoncus",
        step_style
    ))
    
    # Construir o documento
    doc.build(story)
    print("MIP de exemplo gerado com sucesso: output/lorem_mip_example.pdf")

if __name__ == '__main__':
    # Criar diretório output se não existir
    os.makedirs("output", exist_ok=True)
    generate_lorem_mip() 