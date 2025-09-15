from flask import Flask, render_template, request
from models import db, Employee
from sqlalchemy import asc, desc # ф-ии asc и desc используются для указания направления сортировки в запросах к БД.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost/test_database'
db.init_app(app)

@app.route('/')
def all_employees():
    sort_field = request.args.get('sort', 'id') # Столбец для сортировки (по умолчанию 'id')
    order = request.args.get('order', 'asc') # Направление сортировки asc/desc (по умолчанию 'asc')
    search_query = request.args.get('search', '').strip() # Параметр поиска  

    if not hasattr(Employee, sort_field): # Проверка, что поле существует в модели
        sort_field = 'id' # Если поле некорректное - сортируем по id

    sort_order = asc(sort_field) if order == 'asc' else desc(sort_field) # Определение направления сортировки

    query = Employee.query # Базовый запрос
    
    if search_query: # Добавляем поиск, если есть запрос
        query = Employee.query.filter(Employee.full_name.ilike(f'%{search_query}%'))

    employees = query.order_by(sort_order).all()

    return render_template('all_employees9.html', employees=employees,
                           sort_field=sort_field, order=order,
                           search_query=search_query)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()