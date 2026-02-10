from App import app

if __name__ == "__main__":
    # O modo debug=True é essencial enquanto você está aprendendo.
    # Ele reinicia o servidor automaticamente sempre que você salva um arquivo.
    app.run(debug=True)