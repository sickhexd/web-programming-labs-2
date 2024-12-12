from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
import jsonify
lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Бойцовский клуб",
        "title_ru": "Fight Club",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение."
    },
    {
        "title": "Леон",
        "title_ru": "Léon",
        "year": 1994,
        "description": "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, семью которой убили коррумпированные полицейские."
    },
    {
        "title": "Криминальное чтиво",
        "title_ru": "Pulp Fiction",
        "year": 1994,
        "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < len(films):
        return films[id]
    else:
        return "Такого фильма нет!", 200

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < len(films):
        film = request.get_json()
        films[id] = film
        return films[id]
    else:
        return "Такого фильма нет!", 404
    

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    return jsonify({"id": len(films) - 1}), 201

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    if id >= len(films):
        return "Такого фильма нет!", 404
    film = request.get_json()
    if 'description' in film and film['description'] == '':
        return {'error': 'Заполните описание'}, 400
    films[id].update(film)
    return jsonify(films[id])
