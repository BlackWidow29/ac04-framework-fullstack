from app import app, db

if __name__ == "__main__":
    # executa a aplicação
    app.run(debug=True)
    # cria Banco
    db.create_all()

