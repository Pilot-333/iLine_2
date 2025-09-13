from flask import Flask, render_template
from models import db, Employee

app = Flask(__name__)
# URL формата: postgresql://username:password@host/dbname.
# dbname='test_database', user='postgres', password='12345678', host='localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost/test_database'
db.init_app(app)

@app.route('/')
def all_employees():
    employees = Employee.query.all()
    return render_template('all_employees.html', employees=employees)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()