from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Employee
from sqlalchemy import asc, desc # ф-ии asc и desc использ. для указания направления сортировки в запросах к БД.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost/test_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = 'your-secret-key-here' # Для flash-сообщений
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

    all_employees = Employee.query.all() # Получаем всех сотрудников для выпадающего списка

    return render_template('all_employees.html', employees=employees,
                           sort_field=sort_field, order=order,
                           all_employees=all_employees, search_query=search_query)

@app.route('/update_manager/<int:employee_id>', methods=['POST'])
def update_manager(employee_id):
    new_manager_id = request.form.get('manager_id')
    if new_manager_id == 'None':
        new_manager_id = None
    
    employee = Employee.query.get_or_404(employee_id)
    
    try:
        employee.update_manager(new_manager_id)
        flash('Начальник успешно изменен', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
         
    return redirect(request.referrer or url_for('all_employees')) # Перенаправляем обратно с сохранением параметров 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()