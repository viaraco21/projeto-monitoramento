from flask import Flask, jsonify
from models import db, Registro, salvar_dados_da_api
import os
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://{user}:{pw}@{host}:{port}/{db}".format(
        user=os.environ.get("POSTGRES_USER", "usuario"),
        pw=os.environ.get("POSTGRES_PASSWORD", "senha"),
        host=os.environ.get("POSTGRES_HOST", "db"),
        port=5432,
        db=os.environ.get("POSTGRES_DB", "viaipe")
    )
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/importa_api", methods=["POST"])
def importa_api():
    with app.app_context():
        total = salvar_dados_da_api()
    return jsonify({"msg": f"{total} registros importados."})

@app.route("/registros", methods=["GET"])
def listar_registros():
    with app.app_context():
        registros = Registro.query.all()
        return jsonify([reg.to_dict() for reg in registros])

if __name__ == "__main__":
    tentativas = 10
    for i in range(tentativas):
        try:
            with app.app_context():
                db.create_all()
            print("Banco acessível!")
            break
        except Exception as e:
            print(f"Erro ao tentar conectar/postergar inicialização do banco: {e}")
            time.sleep(3)
    app.run(host='0.0.0.0', port=5000)

    app.run(host='0.0.0.0', port=5000, debug=True)    

    def salvar_dados_da_api():
    print("Chamando viaipe.rnp.br/api/norte")  # <- Adicione esse print!
    ...