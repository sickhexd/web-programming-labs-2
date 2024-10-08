from flask import Blueprint, render_template , request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    if not name:  # если name пустое или None
        name = "Неизвестный"
    
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if not age:  # если age пустое или None
        age = "Возраст не указан"
    
    return render_template('lab3.html', name=name,
                            name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Sam', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'red')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
        

    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('form1.html', user=user, 
                           age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('pay.html', drink = drink, price = price)

@lab3.route('/lab3/success_pay', methods=['GET'])
def success_pay():
    drink = request.args.get('drink')
    price = request.args.get('price')
    return render_template('success_pay.html', drink=drink, price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color') 
        background_color = request.form.get('background_color') 
        font_size = request.form.get('font_size')
        font_weight = request.form.get('font_weight')  

        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        resp.set_cookie('background_color', background_color)
        resp.set_cookie('font_size', font_size)
        resp.set_cookie('font_weight', font_weight)
        return resp

    color = request.cookies.get('color', '#000000')
    background_color = request.cookies.get('background_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_weight = request.cookies.get('font_weight', 'normal')

    color = request.cookies.get('color')
    resp = make_response(render_template('settings.html', color=color, background_color=background_color, 
        font_size=font_size, 
        font_weight=font_weight))
    return resp
