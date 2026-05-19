import os
from App import app

if __name__ == "__main__":
    # O modo debug=True é essencial enquanto você está aprendendo.
    # Ele reinicia o servidor automaticamente sempre que você salva um arquivo.
    app.run(
        host=os.getenv('APP_HOST', '127.0.0.1'),
        port=int(os.getenv('APP_PORT', '5000')),
        debug=os.getenv('FLASK_DEBUG', '1') == '1'
    )