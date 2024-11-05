from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from . import db
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = Usuario.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.senha, senha):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha Incorreta', category='erro')
        else:
            flash('Email does not exist', category='erro')

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
        if usuario:
            flash('Email already exists.', category='erro')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='erro')
        elif len(senha1) < 7:
            flash('Passsword must be greater than 7 characters.', category='erro')
        elif len(nome) < 2:
            flash('First name must be greater than 2 characters.', category='erro')
        elif senha1 != senha2:
            flash('Passsword dont match.', category='erro')
        else:
            new_user = Usuario(email=email, nome=nome, senha=generate_password_hash(senha1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(usuario, remember=True)
            flash('Conta criada com sucesso', category='sucesso')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
