from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, 
    Frame, 
    PageTemplate, 
    Image, 
    Paragraph, 
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from pathlib import Path

class MIPDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.page_width, self.page_height = letter
        
        # Margens
        self.top_margin = 1.2 * inch
        self.bottom_margin = 1.2 * inch
        self.left_margin = 1 * inch
        self.right_margin = 1 * inch
        
        # Configurar template da página
        self._create_page_template()
    
    def _create_page_template(self):
        # Frame principal para o conteúdo
        content_frame = Frame(
            self.left_margin,
            self.bottom_margin,
            self.page_width - (self.left_margin + self.right_margin),
            self.page_height - (self.top_margin + self.bottom_margin),
            id='content'
        )
        
        template = PageTemplate(
            'normal',
            [content_frame],
            onPage=self._header_footer
        )
        self.addPageTemplates([template])
    
    def _header_footer(self, canvas, doc):
        canvas.saveState()
        
        # Cabeçalho
        # Logo da empresa (substitua pelo caminho do seu logo)
        logo_path = os.path.join(Path(__file__).parent, 'assets', 'logo.png')
        if os.path.exists(logo_path):
            canvas.drawImage(
                logo_path,
                self.left_margin,
                self.page_height - self.top_margin + 0.2*inch,
                width=1.5*inch,
                height=0.5*inch,
                preserveAspectRatio=True
            )
        
        # Nome da empresa
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(
            self.left_margin + 2*inch,
            self.page_height - self.top_margin + 0.3*inch,
            "Nome da Sua Empresa"
        )
        
        # Linha horizontal no cabeçalho
        canvas.setStrokeColor(colors.gray)
        canvas.line(
            self.left_margin,
            self.page_height - self.top_margin + 0.1*inch,
            self.page_width - self.right_margin,
            self.page_height - self.top_margin + 0.1*inch
        )
        
        # Rodapé
        canvas.setFont('Helvetica', 8)
        # Número da página
        page_num = f"Página {doc.page}"
        canvas.drawString(
            self.page_width - self.right_margin - canvas.stringWidth(page_num, "Helvetica", 8),
            self.bottom_margin - 0.5*inch,
            page_num
        )
        
        # Data de geração
        canvas.drawString(
            self.left_margin,
            self.bottom_margin - 0.5*inch,
            f"Gerado em: {doc.creation_date}"
        )
        
        # Linha horizontal no rodapé
        canvas.line(
            self.left_margin,
            self.bottom_margin - 0.3*inch,
            self.page_width - self.right_margin,
            self.bottom_margin - 0.3*inch
        )
        
        canvas.restoreState() 