import requests
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uf = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    ip = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "uf": self.uf,
            "cidade": self.cidade,
            "nome": self.nome,
            "ip": self.ip,
        }

def salvar_dados_da_api():
    url = "https://viaipe.rnp.br/api/norte"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return 0
    dados = resp.json()
    count = 0
    for item in dados:
        reg = Registro(
            uf=item.get('uf', ''),
            cidade=item.get('cidade', ''),
            nome=item.get('nome', ''),
            ip=item.get('ip', '')
        )
        db.session.add(reg)
        count += 1
    db.session.commit()
    return count