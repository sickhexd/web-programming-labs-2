from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import flash

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Имя не может быть пустым.', 'error')
        else:
            session['name'] = name
            return redirect(url_for('form_age'))
    return render_template('lab9/name.html')
