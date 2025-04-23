from PIL import Image
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.max_width = 1200  # Largura máxima para prints de tela
        self.max_height = 800  # Altura máxima para prints de tela
        self.quality = 85  # Qualidade da compressão JPEG
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.heic', '.heif']
    
    def process_image(self, input_path, output_path=None):
        """
        Processa a imagem para padronizar tamanho e qualidade
        """
        try:
            # Se output_path não for especificado, sobrescreve o arquivo original
            if output_path is None:
                output_path = input_path
            
            # Abrir imagem
            with Image.open(input_path) as img:
                # Converter para RGB se necessário (para imagens PNG com transparência)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Detectar orientação da imagem (para fotos de celular)
                try:
                    exif = img._getexif()
                    if exif:
                        orientation = exif.get(274)  # 274 é o código EXIF para orientação
                        if orientation:
                            # Rotacionar imagem conforme orientação EXIF
                            if orientation == 3:
                                img = img.rotate(180, expand=True)
                            elif orientation == 6:
                                img = img.rotate(270, expand=True)
                            elif orientation == 8:
                                img = img.rotate(90, expand=True)
                except:
                    pass  # Ignora erros de EXIF
                
                # Redimensionar mantendo proporção
                width, height = img.size
                
                # Calcular nova dimensão mantendo proporção
                if width > self.max_width or height > self.max_height:
                    ratio = min(self.max_width/width, self.max_height/height)
                    new_size = (int(width * ratio), int(height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Ajustar contraste e brilho para prints de tela
                if self._is_screenshot(img):
                    from PIL import ImageEnhance
                    # Aumentar contraste levemente para melhorar legibilidade
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.2)
                    # Aumentar nitidez
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.3)
                
                # Salvar imagem processada
                img.save(
                    output_path,
                    'JPEG',
                    quality=self.quality,
                    optimize=True
                )
                
                return output_path
                
        except Exception as e:
            logger.error(f"Erro ao processar imagem {input_path}: {str(e)}")
            return None
    
    def _is_screenshot(self, img):
        """
        Tenta detectar se a imagem é um screenshot baseado em características comuns
        """
        width, height = img.size
        
        # Screenshots geralmente têm dimensões específicas e proporções próximas a monitores
        common_ratios = [
            1.77,  # 16:9
            1.6,   # 16:10
            1.33,  # 4:3
            1.25   # 5:4
        ]
        
        img_ratio = width / height
        # Verifica se a proporção está próxima de alguma proporção comum de tela
        is_common_ratio = any(abs(img_ratio - ratio) < 0.1 for ratio in common_ratios)
        
        # Screenshots geralmente têm cores limitadas e áreas sólidas
        colors = len(img.getcolors(maxcolors=1000)) if img.getcolors(maxcolors=1000) else 1000
        has_limited_colors = colors < 1000
        
        return is_common_ratio and has_limited_colors
    
    def is_supported_format(self, file_path):
        """Verifica se o formato do arquivo é suportado"""
        return Path(file_path).suffix.lower() in self.supported_formats 