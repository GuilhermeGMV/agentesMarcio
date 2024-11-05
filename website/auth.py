from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', text="Testing")


@auth.route('/logout')
def logout():
    return '<p>Logout</p>'


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='erro')
        elif len(password1) < 7:
            flash('Passsword must be greater than 7 characters.', category='erro')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters.', category='erro')
        elif password1 != password2:
            flash('Passsword dont match.', category='erro')
        else:
            flash('Account created successfully.', category='success')
            # add user to db
    return render_template('sign_up.html')
