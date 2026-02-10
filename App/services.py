import base64
import urllib.parse
import re

def clean_svg(svg_str: str) -> str:
    """Limpa e otimiza SVG para uso no Shields.io"""
    # Remover XML declaration
    svg_str = re.sub(r'<\?xml[^?]*\?>', '', svg_str)
    
    # Remover comentários
    svg_str = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    
    # Remover metadados e tags desnecessárias
    svg_str = re.sub(r'<metadata.*?</metadata>', '', svg_str, flags=re.DOTALL)
    svg_str = re.sub(r'<title.*?</title>', '', svg_str, flags=re.DOTALL)
    svg_str = re.sub(r'<desc.*?</desc>', '', svg_str, flags=re.DOTALL)
    
    # Remover atributos width e height da tag svg (manter viewBox)
    svg_str = re.sub(r'(<svg[^>]*)\s+width="[^"]*"', r'\1', svg_str)
    svg_str = re.sub(r'(<svg[^>]*)\s+height="[^"]*"', r'\1', svg_str)
    
    # Remover atributos desnecessários
    svg_str = re.sub(r'\s+fill-rule="[^"]*"', '', svg_str)
    svg_str = re.sub(r'\s+clip-rule="[^"]*"', '', svg_str)
    svg_str = re.sub(r'\s+xmlns:xlink="[^"]*"', '', svg_str)
    
    # Remover espaços múltiplos e quebras de linha
    svg_str = re.sub(r'\s+', ' ', svg_str)
    svg_str = svg_str.strip()
    
    return svg_str

def svg_bytes(upload: bytes) -> bytes:
    # Converter para string para buscar "svg" (case-insensitive)
    upload_str = upload.decode(encoding="utf-8", errors="ignore")
    upload_str_lower = upload_str.lower()
    
    if "<svg" not in upload_str_lower:
        raise ValueError("Arquivo não é SVG")
    
    # Limpar e otimizar SVG
    cleaned_svg = clean_svg(upload_str)
    
    return cleaned_svg.encode('utf-8')

def bytes_to_base64(data: bytes) -> bytes:
   return base64.b64encode(data)

def bytes_to_str(data: bytes) -> str:
    return data.decode(encoding="utf-8", errors="strict")

def url_encode(text: str) -> str:
    return urllib.parse.quote(text, safe='')

def svg_bytes_to_data_url(svg_bytes: bytes) -> str:
    """Converte SVG em base64 para usar como logo no Shields.io"""
    b64_bytes = bytes_to_base64(svg_bytes)
    b64_str = bytes_to_str(b64_bytes)
    # IMPORTANTE: O prefixo data:image/svg+xml;base64, deve ser literal
    # Shields.io NÃO decodifica URL encoding no prefixo do Data URI
    # Apenas retornar o Data URI puro (Base64 já é URL-safe)
    return f"data:image/svg+xml;base64,{b64_str}"

