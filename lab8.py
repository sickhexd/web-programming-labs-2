from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

# Главная страница
@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

# Регистрация с автоматическим логином
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_from = request.form.get('password')

    if not login_form or not password_from:
        return render_template('lab8/register.html', error='Имя пользователя и пароль не могут быть пустыми.')

    # Проверка на существование логина
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хеширование пароля
    password_hash = generate_password_hash(password_from)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический вход
    login_user(new_user, remember=False)  # автоматически залогиним пользователя
    return redirect('/lab8/')

# Страница логина с "запомнить меня"
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_from = request.form.get('password')
    remember_me = 'remember_me' in request.form  # проверка галочки "Запомнить меня"

    if not login_form or not password_from:
        return render_template('lab8/login.html', error='Логин и пароль не могут быть пустыми.')

    user = users.query.filter_by(login=login_form).first()
    if user:
        if check_password_hash(user.password, password_from):
            login_user(user, remember=remember_me)
            return redirect('/lab8/')

    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

# Список статей
@lab8.route('/lab8/articles')
@login_required
def article_list():
    # Получаем список статей из базы данных
    articles_list = articles.query.all()
    return render_template('lab8/articles.html', articles=articles_list)

# Страница для создания статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Заголовок и текст статьи не могут быть пустыми.')

    new_article = articles(title=title, article_text=article_text, user_id=current_user.id)
    db.session.add(new_article)
    db.session.commit()

    flash('Статья успешно создана!', 'success')
    return redirect(url_for('lab8.article_list'))

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является автором статьи
    if article.user_id != current_user.id:
        flash('Вы не можете редактировать чужую статью.', 'error')
        return redirect(url_for('lab8.article_list'))

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, error='Заголовок и текст статьи не могут быть пустыми.')

    article.title = title
    article.article_text = article_text
    db.session.commit()

    flash('Статья успешно отредактирована!', 'success')
    return redirect(url_for('lab8.article_list'))

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является автором статьи
    if article.user_id != current_user.id:
        flash('Вы не можете удалить чужую статью.', 'error')
        return redirect(url_for('lab8.article_list'))

    db.session.delete(article)
    db.session.commit()

    flash('Статья успешно удалена!', 'success')
    return redirect(url_for('lab8.article_list'))




# Логаут
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
