from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from . import db
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if email == 'admin@aa' and senha == '123':
            user = Usuario.query.filter_by(email=email).first()
            if user is None:
                new_user = Usuario(email=email, nome='admin', senha=generate_password_hash(senha, method='pbkdf2:sha256'),
                                   creditos=0)
                db.session.add(new_user)
                db.session.commit()

        user = Usuario.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.senha, senha):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Email ou Senha Inválidos', category='erro')
        else:
            flash('Email ou Senha Inválidos', category='erro')
        return render_template('login.html', user=current_user, email=email)
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        usuario = Usuario.query.filter_by(email=email).first()
        if len(email) == 0 or len(nome) == 0 or len(senha1) == 0 or len(senha2) == 0:
            flash('Preencha todos os campos', category='erro')
        elif usuario:
            flash('O email já está cadastrado', category='erro')
        elif len(senha1) < 6:
            flash('A senha precisa ser maior que 6 caracteres', category='erro')
        elif len(nome) < 2:
            flash('O nome precisa ser maior que 2 caracteres', category='erro')
        elif senha1 != senha2:
            flash('As senhas não são iguais', category='erro')
        else:
            new_user = Usuario(email=email, nome=nome, senha=generate_password_hash(senha1, method='pbkdf2:sha256'),
                               creditos=0)
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada com sucesso', category='sucesso')
            return redirect(url_for('views.home'))
        return render_template('sign_up.html', user=current_user, email=email, nome=nome)
    return render_template('sign_up.html', user=current_user)
