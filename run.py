from app import app
from app.model import Tables

if __name__ == "__main__":
    # cria Banco
    Tables.Base.metadata.create_all(Tables.engine)
    # executa a aplicação
    app.run(debug=True)
