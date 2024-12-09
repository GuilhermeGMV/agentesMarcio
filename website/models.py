from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    resposta = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    conversa_id = db.Column(db.Integer, db.ForeignKey('conversa.id'))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    creditos = db.Column(db.Integer, default=0, nullable=False)
    conversas = db.relationship('Conversa')


class Conversa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship('Note')
    agente_id = db.Column(db.Integer, db.ForeignKey('agente.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    @property
    def messages(self):
        agente = Agente.query.get(self.agente_id)

        messages = [{"role": "system", "content": agente.parametro if agente else "Agente não encontrado"}]

        for note in self.notes:
            messages.append({"role": "user", "content": note.data})
            messages.append({"role": "assistant", "content": note.resposta})

        return messages


class Agente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parametro = db.Column(db.String(10000))
