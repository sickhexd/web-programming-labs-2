from flask import Blueprint, url_for, render_template, abort
lab2 = Blueprint('lab2',__name__)

@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'

@lab2.route('/lab2/a')
def a2():
    return 'без слэша'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@lab2.route('/lab2/flowers/<int:flower_id>')
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
    
@lab2.route('/lab2/add_flower/', defaults={'name': None})
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name:
        flower_list.lab2end(name)
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

@lab2.route('/lab2/flowers')
def all_flowers():
    flower_items = ""
    for flower in flower_list:
        flower_items += f'<li>{flower}</li>'
        
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Все цветы</h1>
            <ul>
                {flower_items}
            </ul>
            <p>Всего цветков: {len(flower_list)}</p>
            <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
        </body>
    </html>
    '''
    
@lab2.route('/lab2/clear_flowers')
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

@lab2.route('/lab2/example')
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

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    pharse = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', pharse=pharse)

@lab2.errorhandler(400)
def bad_request(error):
    return f"<h1>Ошибка 400</h1>", 400

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    return f'''
    <p>Расчет с параметрами:</p>
    <p>{a} + {b} = {a+b}</p>
    <p>{a} - {b} = {a-b}</p>
    <p>{a} x {b} = {a*b}</p>
    <p>{a} / {b} = {a/b}</p>
    <p>{a}<sup>{b}</sup> = {a**b}</p>
'''

@lab2.route('/lab2/books')
def books():
    schedule = [
        {'author': 'Меган Нолан ', 'name': 'Акты отчаяния ', 'genre': 'Роман ', 'pages': '223 стр. '},
        {'author': 'Алексей Иванов ', 'name': 'Бронепараходы ', 'genre': 'Роман ', 'pages': '121 стр. '},
        {'author': 'Илья Мамаев ', 'name': 'Год порно ', 'genre': 'Роман ', 'pages': '323 стр. '},
        {'author': 'Сборник ', 'name': 'Зоопарк в твоей голове ', 'genre': 'Приключения ', 'pages': '431 стр. '},
        {'author': 'Кай Берд ', 'name': 'Оппенгеймер ', 'genre': 'Хоррор ', 'pages': '300 стр. '},
        {'author': 'Джули Оцука ', 'name': 'Пловцы ', 'genre': 'Романтика ', 'pages': '112 стр. '},
        {'author': 'Андрей Подшибякин ', 'name': 'Последний день лета ', 'genre': 'Хоррор-Роман ', 'pages': '1143 стр. '},
        {'author': 'М.Л. Рио ', 'name': 'Словно мы злодеи ', 'genre': 'Детектив ', 'pages': '1223 стр. '},
        {'author': 'Лю Цисинь ', 'name': 'Удержать небо ', 'genre': 'Рассказы ', 'pages': '223 стр. '},
        {'author': 'Мишель Нолан ', 'name': 'Уничтожить ', 'genre': 'Роман ', 'pages': '543 стр. '}
    ]
    return render_template('books.html', schedule=schedule)

@lab2.route('/lab2/cars')
def cars():
    b1 = url_for('static', filename='b1.jpg')
    b2 = url_for('static', filename='b2.jpg')
    b3 = url_for('static', filename='b3.jpg')
    b4 = url_for('static', filename='b4.jpg')
    b5 = url_for('static', filename='b5.jpg')
    cars = [
        {'name': 'BWM X1', 'img': b1, 'info': 'BMW X1 отличается ярким спортивным дизайном, высокими динамическими характеристиками и универсальностью — эта модель идеально подходит для приключений.'},
        {'name': 'BWM X2', 'img': b2, 'info': 'BMW X2 — среднеразмерный кроссовер от немецкого автопроизводителя BMW. Автомобиль был представлен в 2016 году в Париже.'},
        {'name': 'BWM X3', 'img': b3, 'info': 'BMW X3 представлен моделями BMW X3 M40d, M40i, X3 xDrive20i и xDrive20d, X3 xDrive30i и xDrive30d – цены и полное описание модели на официальном сайте BMW'},
        {'name': 'BWM X5', 'img': b4, 'info': 'Оснащенный новыми технологиями, обеспечивающими больше безопасности и максимум динамики на любых покрытиях, BMW X5 является безусловным лидером.'},
        {'name': 'BWM X6', 'img': b5, 'info': 'BMW X6 отличается уникальным внешним видом и спортивной динамичностью благодаря мощному двигателю, точно настроенной подвеске и широкой комплектации'}
    ]
    return render_template('cars.html', cars = cars)