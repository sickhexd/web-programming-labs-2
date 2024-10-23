from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1  or  not x2:
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    elif x2 == '0':
        return render_template('lab4/div.html', error = 'Делить на ноль нельзя!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1:
        return render_template('lab4/sum.html', error = 'Оба поля должны быть заполнены!')
    elif x2 == '':
        x2 = '0'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1:
        x1 = '1'
        x1 = int(x1)
    if not x2:
        x2 = '1'
        x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1  or  not x2:
        return render_template('lab4/sub.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')

@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1  or  not x2:
        return render_template('lab4/exp.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1
    
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей'},
    {'login': 'bob', 'password': '555', 'name': 'БОБ'},
    {'login': 'semen', 'password': '2542', 'name': 'Семен'},
    {'login': 'vladimir', 'password': 'flask-111Q', 'name': 'Владимир'}
]


@lab4.route('/lab4/login', methods = ['get','post'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = session['name']
        else:
            authorized = False
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login='', error='', name=user_name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)    

@lab4.route('/lab4/logout', methods = ['post'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    result = None
    snowflakes = None
    
    if request.method == 'POST':
        try: 
            temp = float(request.form.get('temp'))
            
        except:
            error = "Ошибка: не задана температура или она некорректна."
            return render_template('lab4/fridge.html', error=error)
        

        if temp < -12:
            error = "Не удалось установить температуру — слишком низкое значение."            
        elif temp > -1:
            error = "Не удалось установить температуру — слишком высокое значение."
        elif -12 <= temp <= -9:
            result = f"Установлена температура: {temp}°C"
            snowflakes = 3
        elif -8 <= temp <= -5:
            result = f"Установлена температура: {temp}°C"
            snowflakes = 2
        elif -4 <= temp <= -1:
            result = f"Установлена температура: {temp}°C"
            snowflakes = 1

    return render_template('lab4/fridge.html', 
                           error=error, 
                           result=result, 
                           snowflakes=snowflakes)