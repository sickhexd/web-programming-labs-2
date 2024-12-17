from flask import Blueprint, render_template, request, jsonify, redirect
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_from = request.form.get('password')

    if not login_form or not password_from:
        return render_template('lab8/register.html', error='Имя пользователя и пароль не могут быть пустыми.')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_from)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')