import os
from flask import Flask
from dotenv import load_dotenv

# 1. Carregamos o .env logo no início para que tudo já nasça configurado
load_dotenv() 

# 2. Definimos o app com paths absolutos para templates e static
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# 3. IMPORTANTE: Importar rotas DEPOIS de criar a app para evitar importação circular
from App import routes