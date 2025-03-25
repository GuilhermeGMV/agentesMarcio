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
    numero_fixo = db.Column(db.Integer, nullable=False, unique=False)

    @property
    def messages(self):
        agente = Agente.query.get(self.agente_id)

        messages = [{"role": "system", "content": agente.parametro if agente else "Agente não encontrado"}]

        for note in self.notes:
            messages.append({"role": "user", "content": note.data})
            messages.append({"role": "assistant", "content": note.resposta})

        return messages

    @staticmethod
    def gerar_numero_fixo(user_id):
        """
        Gera o próximo número fixo para o usuário com base nas conversas existentes.
        """
        ultima_conversa = (
            Conversa.query.filter_by(user_id=user_id).order_by(Conversa.numero_fixo.desc()).first()
        )
        return (ultima_conversa.numero_fixo + 1) if ultima_conversa else 1


class Agente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    parametro = db.Column(db.String(10000), nullable=True)

