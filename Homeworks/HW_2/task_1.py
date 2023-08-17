"""
Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя,
а также будет произведено перенаправление на страницу приветствия,
где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти»,
при нажатии на которую будет удалён cookie-файл с данными пользователя
и произведено перенаправление на страницу ввода имени и электронной почты.
"""
import secrets
from flask import Flask, render_template, request, redirect, make_response, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex()


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    response = make_response(redirect('/hello'))
    response.set_cookie('username', username)
    return response


@app.route('/hello')
def hello():
    username = request.cookies.get('username')
    if username:
        return render_template("hello.html", username=username)
    return redirect("/")


@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('username')
    return response


if __name__ == '__main__':
    app.run(debug=True)

