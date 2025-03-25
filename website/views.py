from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
from . import db
from .models import Note, Conversa, Agente

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    conversa_id = request.args.get('conversa_id', type=int)
    agente_id = request.args.get('agente_id', default=None, type=int)

    conversa = (
        Conversa.query.filter_by(id=conversa_id, user_id=current_user.id).first()
        if conversa_id
        else None
    )

    agente = None
    if conversa:
        agente = Agente.query.get(conversa.agente_id)
    agenteSelecionado = bool(agente_id or conversa)

    print("Request args:", request.args)
    print("Request form:", request.form)
    print("Agente ID recebido:", agente_id)

    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) >= 1:
            if not conversa:
                novo_numero_fixo = Conversa.gerar_numero_fixo(current_user.id)
                conversa = Conversa(agente_id=agente_id, user_id=current_user.id, numero_fixo=novo_numero_fixo)
                db.session.add(conversa)
                db.session.flush()

            new_note = Note(data=note, resposta='Resposta do assistente aqui', conversa_id=conversa.id)
            db.session.add(new_note)
            db.session.commit()

            return redirect(url_for('views.home', conversa_id=conversa.id))

    user_conversas = (
        Conversa.query.filter_by(user_id=current_user.id)
        .order_by(Conversa.numero_fixo.asc())
        .all()
    )
    user_conversas_with_numbers = [
        {
            'numero': conversa.numero_fixo,
            'id': conversa.id,
            'agente_nome': Agente.query.get(conversa.agente_id).nome if conversa.agente_id else "Sem agente"
        }
        for conversa in user_conversas
    ]

    agentes = Agente.query.all()

    return render_template(
        'home.html',
        user_conversas=user_conversas_with_numbers,
        conversa=conversa,
        agente=agente,
        agenteSelecionado=agenteSelecionado,
        agentes=agentes,
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
