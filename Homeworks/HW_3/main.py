"""
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email",
"Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе
данных, а пароль должен быть зашифрован.
"""

import secrets
from flask_wtf import CSRFProtect
from flask import Flask, render_template, request
from forms import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)


@app.route('/')
def index():
    return'Hi!'


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
        if existing_user:
            error_msg = 'This username or email already exists.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)
        user = User(name=name, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return "Registration is successfully finished."
    return render_template('register.html', form=form)

