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

    # Obtém a conversa específica se o ID foi passado
    conversa = (
        Conversa.query.filter_by(id=conversa_id, user_id=current_user.id, agente_id=agente_id).first()
        if conversa_id
        else None
    )

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) >= 1:
            # Cria uma nova conversa se não houver uma ativa
            if not conversa:
                novo_numero_fixo = Conversa.gerar_numero_fixo(current_user.id)
                conversa = Conversa(agente_id=agente_id, user_id=current_user.id, numero_fixo=novo_numero_fixo)
                db.session.add(conversa)
                db.session.flush()  # Garante que a conversa tenha um ID antes de usar

            # Cria uma nova nota associada à conversa
            new_note = Note(data=note, resposta='Resposta do assistente aqui', conversa_id=conversa.id)
            db.session.add(new_note)
            db.session.commit()

            return redirect(url_for('views.home', conversa_id=conversa.id))

    # Obtém todas as conversas do usuário, incluindo o número fixo
    user_conversas = (
        Conversa.query.filter_by(user_id=current_user.id)
        .order_by(Conversa.numero_fixo.asc())  # Ordena pelas conversas na ordem dos números fixos
        .all()
    )
    user_conversas_with_numbers = [
        {'numero': conversa.numero_fixo, 'id': conversa.id} for conversa in user_conversas
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


@views.route('/delete-conversa', methods=['POST'])
@login_required
def delete_conversa():
    conversa_id = request.form.get('conversa_id')

    if not conversa_id:
        flash('ID da conversa não fornecido.', 'error')
        return redirect(url_for('views.home'))

    conversa = Conversa.query.filter_by(id=conversa_id, user_id=current_user.id).first()
    if not conversa:
        flash('Erro 404: Conversa não encontrada ou você não tem permissão para deletá-la', 'error')
        return redirect(url_for('views.home'))

    for note in conversa.notes:
        db.session.delete(note)
    db.session.delete(conversa)
    db.session.commit()
    flash('Conversa deletada com sucesso', 'success')

    return redirect(url_for('views.home'))
