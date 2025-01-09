from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
from . import db
from .models import Note, Conversa

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    conversa_id = request.args.get('conversa_id', type=int)
    agente_id = request.args.get('agente_id', default=1, type=int)

    conversa = (
        Conversa.query.filter_by(id=conversa_id, user_id=current_user.id, agente_id=agente_id).first()
        if conversa_id
        else None
    )

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) >= 1:
            if not conversa:
                conversa = Conversa(agente_id=agente_id, user_id=current_user.id)
                db.session.add(conversa)
                db.session.flush()  # Garante que a conversa tenha um ID para vincular a mensagem

            new_note = Note(data=note, resposta='Resposta do assistente aqui', conversa_id=conversa.id)
            db.session.add(new_note)
            db.session.commit()

            return redirect(url_for('views.home', conversa_id=conversa.id))

    user_conversas = Conversa.query.filter_by(user_id=current_user.id).all()
    user_conversas_with_numbers = [
        {'numero': idx + 1, 'id': conversa.id} for idx, conversa in enumerate(user_conversas)
    ]

    return render_template(
        'home.html',
        user_conversas=user_conversas_with_numbers,
        conversa=conversa,
        user=current_user
    )


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


@views.route('/delete-conversa', methods=['POST', 'GET'])
@login_required
def delete_conversa():
    print(request.method)
    conversa_id = request.form.get('conversa_id')

    conversa = Conversa.query.filter_by(id=conversa_id, user_id=current_user.id).first()
    if not conversa:
        return flash('erro 404: Conversa não encontrada ou você não tem permissão para deletá-la'), 404

    for note in conversa.notes:
        db.session.delete(note)
    db.session.delete(conversa)
    db.session.commit()
    flash('Conversa deletada com sucesso')

    return flash('Conversa deletada com sucesso')
