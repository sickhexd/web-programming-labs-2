from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")

def start():
    return """<!doctype html> \
        <html> \
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a><br>
                <a href="/lab1/oak">Oak</a><br>
                <a href="/lab1/counter">counter</a><br>
                <a href="/info">info</a><br>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/web")
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



@app.route("/author")
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
                <a href="/">start</a>
            </body>
        </html>"""


@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename = "oak.png")
    return '''
    <!doctype>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src="'''+ path +'''">
                <a href="/">start</a>
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
                <a href="/">start</a>
            </body>
        </html>
    '''

@app.route("/info")
def info():
    return redirect("/author")

@app.errorhandler(404)
def not_found(err):
    return "Такой страницы нет", 404