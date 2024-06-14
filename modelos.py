from escola import db

#Definição dos modelos
class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    voto = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name