from flask import Flask, url_for, redirect, render_template, abort, session
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)

app.secret_key = 'секретынй код'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)

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

