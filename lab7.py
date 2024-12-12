from flask import Blueprint, render_template, request, jsonify
lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {"title": "Бойцовский клуб", "title_ru": "Fight Club", "year": 1999, "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией."},
    {"title": "Леон", "title_ru": "Léon", "year": 1994, "description": "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, семью которой убили коррумпированные полицейские."},
    {"title": "Криминальное чтиво", "title_ru": "Pulp Fiction", "year": 1994, "description": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса."}
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < len(films):
        return jsonify(films[id])
    else:
        return jsonify({"error": "Такого фильма нет!"}), 404

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    return jsonify({"id": len(films) - 1}), 201

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < len(films):
        del films[id]
        return '', 204
    else:
        return jsonify({"error": "Такого фильма нет!"}), 404

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    if id >= len(films) or id < 0:
        return jsonify({"error": "Такого фильма нет!"}), 404
    film_data = request.get_json()
    if not film_data:
        return jsonify({"error": "Нет данных для обновления"}), 400
    # Проверяем, что все необходимые поля присутствуют в запросе
    if 'title' not in film_data or 'title_ru' not in film_data or 'year' not in film_data or 'description' not in film_data:
        return jsonify({"error": "Все поля должны быть заполнены: title, title_ru, year, description"}), 400
    if film_data['description'] == '':
        return jsonify({'error': 'Заполните описание'}), 400
    # Обновляем данные фильма
    films[id] = film_data
    return jsonify(films[id])

