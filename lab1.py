from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1',__name__)

@lab1.route("/lab1")
def lab():
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
                <h1>Список роутов</h1>
                <li><a href="/lab1/author">author</a></li>
                <li><a href="/lab1/oak">Oak</a></li>
                <li><a href="/lab1/counter">counter</a></li>
                <li><a href="/lab1/info">info</a></li>
                <li><a href="/lab1/web">web</a></li>
                <li><a href="/lab1/zxc">404</a></li>
                <li><a href="/lab1/400">400</a></li>
                <li><a href="/lab1/401">401</a></li>
                <li><a href="/lab1/402">402</a></li>
                <li><a href="/lab1/403">403</a></li>
                <li><a href="/lab1/405">405</a></li>
                <li><a href="/lab1/500">500</a></li>
                <li><a href="/lab1/newroute">Monkey</a></li>
            </body>
        </html>"""

@lab1.route("/lab1/web")
def web():
    return """<!doctype html> \
        <html> \
            <body>
                <a href="/">start</a>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@lab1.route("/lab1/author")
def author():
    name = "Антонов Семен Андреевич"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype>
        <html>
            <body>
                <p>Студент: """+ name +"""</p>
                <p>Группа: """+ group +"""</p>
                <p>Факультет: """+ faculty +"""</p>
            </body>
        </html>"""

@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename = "lab1/oak.png")
    return f'''
    <!doctype>
        <html>
            <head>
                <link rel="stylesheet" href="{url_for('static', filename = "lab1/lab1.css")}">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="'''+ path +'''">
            </body>
        </html>
    '''

count=0
@lab1.route('/lab1/counter')
def counter():
    global count
    count +=1
    return f'''
    <!doctype>
        <html>
            <body>
                Сколько раз вы сюда заходили:{count}<br>
                <a href="/lab1/refresh">refresh</a>
            </body>
        </html>
    '''

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/refresh")
def refresh():
    global count
    count = 0
    return redirect("/lab1/counter")

@lab1.route('/lab1/newroute')
def newroute():
    path = url_for("static", filename = "lab1/monk.png")
    return f'''
    <!DOCTYPE html>
    <head>
        <title>newroute</title>
        <link rel="stylesheet" href="{url_for('static', filename = "lab1/lab1.css")}">
    </head>
    <body>
        <div class="error-container">
            <h1>Шимпанзе</h1>
            <p>Шимпанзе́ (лат. Pan) — род из семейства гоминид отряда приматов. К нему относятся два вида: обыкновенный шимпанзе (Pan troglodytes) и карликовый шимпанзе (Pan paniscus), также известный под названием бонобо[2][3]. Оба вида находятся под угрозой вымирания согласно Красной книге МСОП, а в 2017 году Конвенция по сохранению мигрирующих видов диких животных выбрали обыкновенного шимпанзе для особой защиты[4].</p>
            <img style="width: 50%;" src="'''+ path +'''"> 
        </div>
    </body>
    </html>
''', 200, {'Content-Language': 'ru-Ru', 'Link': 'https://example.com', 'Info': 'Info'}

@lab1.route('/lab1/400')
def bad_request():
    return "400 BadRequest!", 400

@lab1.route('/lab1/401')
def Unauthorized():
    return "401 Unauthorized", 401

@lab1.route('/lab1/402')
def Payment_Required():
    return "402 Payment Required", 402

@lab1.route('/lab1/403')
def Forbidden():
    return "403 Forbidden", 403

@lab1.route('/lab1/405')
def Method_Not_Allowed():
    return "405 Method Not Allowed", 405

@lab1.route('/lab1/500')
def err_500():
    return 1/0