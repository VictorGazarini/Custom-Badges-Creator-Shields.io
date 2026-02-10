import os
from flask import Flask
from dotenv import load_dotenv

# 1. Carregamos o .env logo no início para que tudo já nasça configurado
load_dotenv() 

# 2. Definimos o app com paths absolutos para templates e static
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Security hardening
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024  # 200KB

@app.after_request
def set_security_headers(response):
	response.headers['X-Content-Type-Options'] = 'nosniff'
	response.headers['X-Frame-Options'] = 'DENY'
	response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
	response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

	csp = (
		"default-src 'self'; "
		"script-src 'self' https://cdn.jsdelivr.net; "
		"style-src 'self' https://cdn.jsdelivr.net; "
		"img-src 'self' data: https://img.shields.io; "
		"connect-src 'self'; "
		"font-src 'self' data:; "
		"object-src 'none'; "
		"base-uri 'self'; "
		"frame-ancestors 'none'"
	)
	response.headers['Content-Security-Policy'] = csp
	return response

# 3. IMPORTANTE: Importar rotas DEPOIS de criar a app para evitar importação circular
from App import routes