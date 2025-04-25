from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, 
    Frame, 
    PageTemplate, 
    Image, 
    Paragraph, 
    Spacer,
    NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
import os
from pathlib import Path

# Definindo as cores da empresa
RAMAL_BLUE = colors.HexColor('#00517C')

class MIPDocTemplate(BaseDocTemplate):
    def __init__(self, filename, title="", **kwargs):
        super().__init__(filename, **kwargs)
        self.page_width, self.page_height = letter
        self.title = title
        
        # Margens padrão
        self.content_left_margin = 1 * inch
        self.content_right_margin = 1 * inch
        self.top_margin = 2.5 * inch  # Espaço para o logo na primeira página
        self.bottom_margin = 1 * inch
        
        # Configurar templates de página
        self._create_page_templates()
    
    def _create_page_templates(self):
        # Frame para primeira página (com cabeçalho)
        first_page_frame = Frame(
            self.content_left_margin,
            self.bottom_margin,
            self.page_width - (self.content_left_margin + self.content_right_margin),
            self.page_height - (self.top_margin + self.bottom_margin),
            id='firstPage'
        )
        
        # Frame para páginas normais (sem cabeçalho e sem rodapé)
        normal_frame = Frame(
            self.content_left_margin,
            self.bottom_margin,
            self.page_width - (self.content_left_margin + self.content_right_margin),
            self.page_height - (2 * self.bottom_margin),  # Margem superior menor
            id='normal'
        )
        
        # Frame para última página (sem cabeçalho, com rodapé)
        last_page_frame = Frame(
            self.content_left_margin,
            4.5 * inch,  # Espaço para o rodapé
            self.page_width - (self.content_left_margin + self.content_right_margin),
            self.page_height - (2 * self.bottom_margin) - 3.5 * inch,  # Ajustado para o rodapé
            id='lastPage'
        )
        
        # Template para primeira página
        first_template = PageTemplate(
            'FirstPage',
            [first_page_frame],
            onPage=self._header
        )
        
        # Template para páginas normais
        normal_template = PageTemplate(
            'Normal',
            [normal_frame],
            onPage=self._empty  # Sem cabeçalho
        )
        
        # Template para última página
        last_template = PageTemplate(
            'LastPage',
            [last_page_frame],
            onPage=self._footer  # Apenas rodapé
        )
        
        self.addPageTemplates([first_template, normal_template, last_template])
    
    def _empty(self, canvas, doc):
        """Página sem cabeçalho nem rodapé"""
        pass
    
    def _header(self, canvas, doc):
        """Apenas cabeçalho para primeira página"""
        canvas.saveState()
        
        # Logo da empresa - colado na borda
        logo_path = os.path.join(Path(__file__).parent, 'assets', 'logo.png')
        if os.path.exists(logo_path):
            canvas.drawImage(
                logo_path,
                0,  # Começa na borda esquerda
                self.page_height - 2*inch,  # 2 polegadas do topo
                width=self.page_width,  # Largura total
                height=2*inch,
                preserveAspectRatio=True
            )
        
        # Título do documento
        if self.title:
            canvas.setFont('Helvetica-Bold', 14)
            canvas.setFillColor(colors.black)
            canvas.drawString(
                self.content_left_margin,
                self.page_height - self.top_margin + 0.2*inch,
                f"MIP - {self.title}"
            )
        
        canvas.restoreState()
    
    def _footer(self, canvas, doc):
        """Apenas rodapé para última página"""
        canvas.saveState()
        
        footer_start = 4 * inch
        
        # Título do Suporte
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(colors.HexColor('#3182CE'))
        canvas.drawCentredString(
            self.page_width/2,
            footer_start,
            "Suporte Ramal Virtual"
        )

        # Texto de contato urgente
        canvas.setFont('Helvetica', 11)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString(
            self.page_width/2,
            footer_start - 0.4*inch,
            "Se precisar de urgência, ligue para o telefone (11) 3090-0900."
        )

        # QR Code
        qr_size = 2.835*inch
        qr_code = qr.QrCodeWidget('https://suporte.ramalvirtual.com.br')
        qr_bounds = qr_code.getBounds()
        qr_width = qr_bounds[2] - qr_bounds[0]
        qr_height = qr_bounds[3] - qr_bounds[1]
        
        d = Drawing(qr_size, qr_size, transform=[qr_size/qr_width, 0, 0, qr_size/qr_height, 0, 0])
        d.add(qr_code)
        
        renderPDF.draw(d, canvas, 
            self.page_width/2 - qr_size/2,
            footer_start - 3*inch
        )

        # Informações da empresa
        canvas.setFont('Helvetica', 9)
        footer_text = "www.ramalvirtual.com.br    CEP:07021-050    Rua Santa Rita de Cássia 155"
        canvas.drawCentredString(
            self.page_width/2,
            0.5*inch,
            footer_text
        )
        
        canvas.restoreState()