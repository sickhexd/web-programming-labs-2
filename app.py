from flask import Flask, url_for, redirect, render_template, abort
app = Flask(__name__)

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
                
            </body>
        </html>"""

@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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



@app.route("/lab1/author")
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


@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename = "oak.png")
    return f'''
    <!doctype>
        <html>
            <head>
                <link rel="stylesheet" href="{url_for('static', filename = "lab1.css")}">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="'''+ path +'''">
            </body>
        </html>
    '''

count=0
@app.route('/lab1/counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/refresh")
def refresh():
    global count
    count = 0
    return redirect("/lab1/counter")

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

@app.route('/lab1/400')
def bad_request():
    return "400 BadRequest!", 400

@app.route('/lab1/401')
def Unauthorized():
    return "401 Unauthorized", 401

@app.route('/lab1/402')
def Payment_Required():
    return "402 Payment Required", 402

@app.route('/lab1/403')
def Forbidden():
    return "403 Forbidden", 403

@app.route('/lab1/405')
def Method_Not_Allowed():
    return "405 Method Not Allowed", 405

@app.errorhandler(500)
def error500(err):
    return "Внутренняя ошибка сервера!", 500

@app.route('/lab1/500')
def err_500():
    return 1/0

@app.route('/lab1/newroute')
def newroute():
    path = url_for("static", filename = "monk.png")
    return f'''
    <!DOCTYPE html>
    <head>
        <title>newroute</title>
        <link rel="stylesheet" href="{url_for('static', filename = "lab1.css")}">
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

@app.route('/lab2/a/')
def a():
    return 'со слэшем'

@app.route('/lab2/a')
def a2():
    return 'без слэша'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
        <!doctype html>
        <html>
            <body>
                <h1>Цветок: {flower_name}</h1>
                <p><a href="/lab2/flowers">Список всех цветков</a></p>
            </body>
        </html>
        '''
    
@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name:
        flower_list.append(name)
        return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветков: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
        </body>
    </html>
    '''
    else:
        abort(400, description="Вы не задали имя цветка")

@app.route('/lab2/flowers')
def all_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Все цветы</h1>
            <ul>
                {''.join(f'<li>{flower}</li>' for flower in flower_list)}
            </ul>
            <p>Всего цветков: {len(flower_list)}</p>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
        </body>
    </html>
    '''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Список цветов очищен!</h1>
            <p><a href="/lab2/flowers">Список всех цветков</a></p>
        </body>
    </html>
    '''


@app.route('/lab2/example')
def example():
    course = '3'
    lab_num = '2'
    group = 'ФБИ-21'
    name = 'Антонов Семен'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}

    ]
    return render_template('example.html', name = name, 
                           course = course, 
                           lab_num = lab_num, 
                           group=group, fruits = fruits )

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    pharse = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', pharse=pharse)

@app.errorhandler(400)
def bad_request(error):
    return f"<h1>Ошибка 400</h1>", 400


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    return f'''
    <p>Расчет с параметрами:</p>
    <p>{a} + {b} = {a+b}</p>
    <p>{a} - {b} = {a-b}</p>
    <p>{a} x {b} = {a*b}</p>
    <p>{a} / {b} = {a/b}</p>
    <p>{a}<sup>{b}</sup> = {a**b}</p>
'''