from flask import Flask, url_for, redirect, render_template, abort, session
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
import os
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
from flask_login import LoginManager
from db.models import users

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'antonov_orm'
    db_user = 'antonov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "antonov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

@app.route("/")
def start():
    return """<!doctype html> 
        <html> 
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title>
            </head>
            <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных<br>
                Антонов Семен, ФБИ-21
            </header>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1">Лабораторная работа 1</a><br>
                <a href="/lab2">Лабораторная работа 2</a><br>
                <a href="/lab3">Лабораторная работа 3</a><br>
                <a href="/lab4">Лабораторная работа 4</a><br>
                <a href="/lab5">Лабораторная работа 5</a><br>
                
            </body>
        </html>"""

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename = "404.png")
    return f'''
    <!DOCTYPE html>
    <head>
        <title>404 Error</title>
        <link rel="stylesheet" href="{url_for('static', filename = "lab1.css")}">
    </head>
    <body>
        <div class="error-container">
            <h1>Oops! Page not found.</h1>
            <p>The page you're looking for doesn't exist or has been moved.</p>
            <img src="'''+ path +'''"> 
        </div>
    </body>
    </html>
''', 404

@app.errorhandler(500)
def error500(err):
    return "Внутренняя ошибка сервера!", 500

