from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from . import db
from .models import Note, Conversa

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    conversa = Conversa.query.filter_by(id=1).first()

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) >= 1:
            conversa = Conversa.query.filter_by(user_id=current_user.id, agente_id=1).first()

            if not conversa:
                conversa = Conversa(agente_id=1, user_id=current_user.id)
                db.session.add(conversa)
                db.session.flush()

            new_note = Note(data=note, resposta='Resposta do assistente aqui', conversa_id=conversa.id)
            db.session.add(new_note)

            db.session.commit()

    return render_template('home.html', user=current_user, conversa=conversa)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
