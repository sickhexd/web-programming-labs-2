from flask import Blueprint, render_template, request, redirect, session, current_app
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
            host = '127.0.0.1',
            database = 'antonov_database',
            user = 'antonov_database',
            password = '123'
        )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn,cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()






@lab5.route('/lab5/login', methods = ['get','post'])
def login():
    if request.method == 'get':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error = 'Заполните все поля!')

    conn, cur = db_coonect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"select login from users where login=%s;", (login))
    else:
        cur.execute(f"select login from users where login=?;", (login))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль не верны!')
    
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html', error='Логин и/или пароль не верны!')

    session['login'] = login
    db_close(conn,cur)
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
        cur.execute(f"select login from users where login=?;", (login))
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
    cur.execute(f"select id from users where login='{login}';")
    user_id = cur.fetchone()['id']
    cur.execute(f"select * from articles where user_id='{user_id}';")
    articles = cur.fetchall()
    db_close(conn,cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/create', methods = ['get','post'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_coonect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"select login from users where login=%s;", (login))
    else:
        cur.execute(f"select login from users where login=?;", (login))
    user_id = cur.fetchone()['id']

    cur.execute(f"insert into articles(user_id, title, article_text)\
                values ({user_id}, '{title}', '{article_text}');")
    db_close(conn, cur)
    return redirect("/lab5")