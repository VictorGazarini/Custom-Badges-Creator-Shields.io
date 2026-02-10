from flask import render_template, request
from App import app
from App.services import svg_bytes_to_data_url, svg_bytes
import logging
import urllib.parse

# Configurar logging
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Coletar todos os parâmetros do formulário
        label = request.form.get('label', '').strip()
        message = request.form.get('message', '').strip()
        color = request.form.get('color', 'brightgreen').strip()
        style = request.form.get('style', 'for-the-badge').strip()
        label_color = request.form.get('labelColor', '').strip()
        logo_simple = request.form.get('logo', '').strip()
        logo_color = request.form.get('logoColor', '').strip()
        logo_size = request.form.get('logoSize', '').strip()
        arquivo_storage = request.files.get('file')
        
        # Validação: message é obrigatório
        if not message:
            return """
            <div class="glass-alert-error flex items-center gap-3 p-4 rounded-lg">
                <span class="text-2xl">✕</span>
                <div>
                    <p class="font-bold">Erro: Message obrigatório</p>
                    <p class="text-sm opacity-90">O campo Message deve ser preenchido</p>
                </div>
            </div>
            """, 400
        
        # Construir badgeContent (label-message-color ou message-color)
        if label:
            badge_content = f"{label}-{message}-{color}"
        else:
            badge_content = f"{message}-{color}"
        
        # Construir URL base
        badge_url = f"https://img.shields.io/badge/{badge_content}"
        
        # Adicionar query parameters
        params = {}
        if style:
            params['style'] = style
        if label_color:
            params['labelColor'] = label_color
        if logo_color:
            params['logoColor'] = logo_color
        if logo_size:
            params['logoSize'] = logo_size
        
        # Processar logo (Simple Icons ou Custom SVG)
        logo_value = None
        if arquivo_storage and arquivo_storage.filename:
            # Custom SVG Upload
            if not arquivo_storage.filename.lower().endswith('.svg'):
                return """
                <div class="glass-alert-error flex items-center gap-3 p-4 rounded-lg">
                    <span class="text-2xl">✕</span>
                    <div>
                        <p class="font-bold">Erro: Tipo de arquivo inválido</p>
                        <p class="text-sm opacity-90">Apenas arquivos SVG são permitidos</p>
                    </div>
                </div>
                """, 400
            
            dados_binarios = arquivo_storage.read()
            
            if len(dados_binarios) == 0:
                return """
                <div class="glass-alert-error flex items-center gap-3 p-4 rounded-lg">
                    <span class="text-2xl">✕</span>
                    <div>
                        <p class="font-bold">Erro: Arquivo vazio</p>
                        <p class="text-sm opacity-90">O arquivo SVG não contém dados</p>
                    </div>
                </div>
                """, 400
            
            logo_value = svg_bytes_to_data_url(svg_bytes(dados_binarios))
        elif logo_simple:
            # Simple Icons slug
            logo_value = logo_simple
        
        if logo_value:
            params['logo'] = logo_value
        
        # Construir URL completa
        if params:
            query_string = urllib.parse.urlencode(params, safe=':,/')
            full_url = f"{badge_url}?{query_string}"
        else:
            full_url = badge_url
        
        # Retornar preview e URL
        return f"""
        <div class="space-y-4">
            <div class="glass-alert-success flex items-center gap-3 p-4 rounded-lg">
                <span class="text-2xl">✓</span>
                <div>
                    <p class="font-bold">Badge gerado com sucesso!</p>
                    <p class="text-sm opacity-90">URL pronta para uso</p>
                </div>
            </div>
            
            <!-- Preview do Badge -->
            <div class="glass-preview gradient-border p-6 rounded-lg">
                <label class="block text-sm font-semibold text-gray-200 mb-3">Preview:</label>
                <div class="flex items-center justify-center p-6 bg-white/5 rounded-lg">
                    <img src="{full_url}" 
                         alt="Badge Preview" 
                         class="max-w-full h-auto">
                </div>
            </div>
            
            <div class="space-y-3">
                <label class="block text-sm font-semibold text-gray-200">URL Completa:</label>
                <div class="relative">
                    <code id="url-resultado" class="glass-code block px-4 py-3 rounded-lg text-xs font-mono overflow-x-auto whitespace-pre-wrap break-all max-h-40">{full_url}</code>
                </div>
                <button class="btn-copiar btn-primary w-full" type="button">Copiar URL</button>
            </div>
            
            <!-- Markdown Preview -->
            <div class="space-y-3">
                <label class="block text-sm font-semibold text-gray-200">Código Markdown:</label>
                <div class="relative">
                    <code class="glass-code block px-4 py-3 rounded-lg text-xs font-mono overflow-x-auto whitespace-pre-wrap break-all">![Badge]({full_url})</code>
                </div>
            </div>
        </div>
        """

    except ValueError as e:
        logger.warning(f"Validação SVG falhou: {str(e)}")
        return f"""
        <div class="glass-alert-error flex items-center gap-3 p-4 rounded-lg">
            <span class="text-2xl">✕</span>
            <div>
                <p class="font-bold">Erro de Validação</p>
                <p class="text-sm opacity-90">{str(e)}</p>
            </div>
        </div>
        """, 400
        
    except Exception as e:
        logger.error(f"Erro ao processar badge: {str(e)}", exc_info=True)
        return f"""
        <div class="glass-alert-error flex items-center gap-3 p-4 rounded-lg">
            <span class="text-2xl">⚠</span>
            <div>
                <p class="font-bold">Erro ao processar badge</p>
                <p class="text-sm opacity-90">Tente novamente ou verifique os campos</p>
            </div>
        </div>
        """, 500