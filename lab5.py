from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_coonect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='antonov_database',
            user='antonov_database',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()






@lab5.route('/lab5/login', methods=['get', 'post'])
def login():
    if request.method == 'get':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля!')

    conn, cur = db_coonect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, password FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT login, password FROM users WHERE login = ?", (login,))

    user = cur.fetchone()
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль не верны!')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)













@lab5.route('/lab5/register', methods=['get','post'])
def register():

    if request.method == 'get':
        return render_template('lab5/register.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error = 'Заполните все поля!')
    
    conn, cur = db_coonect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"select login from users where login=%s;", (login))
    else:
        cur.execute("SELECT login FROM users WHERE login = ?", (login,))

    if cur.fetchone():
        db_close(conn,cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"insert into users (login, password) values (%s, %s);", (login, password_hash))
    else:
        cur.execute(f"insert into users (login, password) values (?, ?);", (login, password_hash))
    db_close(conn,cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_coonect()
    
    # Получаем id пользователя по его логину
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/articles.html', error='Пользователь не найден')

    user_id = user['id']
    
    # Получаем статьи пользователя
    cur.execute("SELECT * FROM articles WHERE user_id = ?", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)

    # Если нет статей, выводим сообщение
    if not articles:
        return render_template('lab5/articles.html', message='У вас нет ни одной статьи.')

    return render_template('lab5/articles.html', articles=articles)


@lab5.route('/lab5/create', methods=['get', 'post'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')


    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля: тема и текст статьи.')
    
    conn, cur = db_coonect()


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error='Пользователь не найден')

    user_id = user['id']


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                    (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", 
                    (user_id, title, article_text))

    db_close(conn, cur)
    return redirect("/lab5")


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')


@lab5.route('/lab5/edit/<int:article_id>/', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_coonect()
    if not conn or not cur:
        return render_template('lab5/create_article.html', error='Ошибка подключения к базе данных')

    if request.method == 'GET':
        # Получаем статью для редактирования
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (article_id, login))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", (article_id, login))

        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return render_template('lab5/create_article.html', error='Статья не найдена или вы не авторизованы для её редактирования')

        # Отправляем статью в шаблон для редактирования
        return render_template('lab5/create_article.html', article=article)

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # Если checkbox "is_public" установлен, то он равен True

    # Валидация формы
    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля', 
                               article={'id': article_id, 'title': title, 'article_text': article_text, 'is_public': is_public})

    # Обновляем статью в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", 
                    (title, article_text, is_public, article_id, login))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_public=? WHERE id=? AND login_id=(SELECT id FROM users WHERE login=?);", 
                    (title, article_text, is_public, article_id, login))

    db_close(conn, cur)

    # Перенаправляем на список статей
    return redirect(url_for('lab5.list'))


