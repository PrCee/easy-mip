from document_template import MIPDocTemplate
from reportlab.platypus import Paragraph, Spacer, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_test_mip():
    # Criar o documento
    doc = MIPDocTemplate("test_mip.pdf", title="Teste de Formatação")
    story = []
    styles = getSampleStyleSheet()
    
    # Primeira página começa com o template FirstPage por padrão
    
    # Conteúdo da primeira página
    story.append(Paragraph("Primeira Página - Com Cabeçalho", styles['Heading1']))
    for _ in range(5):
        story.append(Paragraph(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10,
            styles['Normal']
        ))
    
    # Mudar para o template normal na próxima página
    story.append(NextPageTemplate('Normal'))
    story.append(Spacer(1, 20))
    
    # Segunda página (sem cabeçalho/rodapé)
    story.append(Paragraph("Segunda Página - Sem Cabeçalho", styles['Heading1']))
    for _ in range(5):
        story.append(Paragraph(
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 10,
            styles['Normal']
        ))
    
    # Mudar para o template da última página
    story.append(NextPageTemplate('LastPage'))
    story.append(Spacer(1, 20))
    
    # Última página (com rodapé)
    story.append(Paragraph("Última Página - Com Rodapé", styles['Heading1']))
    for _ in range(5):
        story.append(Paragraph(
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco. " * 10,
            styles['Normal']
        ))
    
    # Construir o documento
    doc.build(story)

if __name__ == '__main__':
    generate_test_mip()
