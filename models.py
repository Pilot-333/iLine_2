from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees' # Указываем имя существующей таблицы
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    post = db.Column(db.String(200))
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id')) # Самоссылающаяся связь
    manager = relationship("Employee", remote_side=[id], backref="subordinates")

    def update_manager(self, new_manager_id):
        """Обновляет начальника сотрудника"""
        if new_manager_id == self.id:
            raise ValueError("Сотрудник не может быть своим начальником")
        
        if new_manager_id is not None:
            new_manager = Employee.query.get(new_manager_id)
            if not new_manager:
                raise ValueError("Указанный начальник не существует")
        
        self.manager_id = new_manager_id
        db.session.commit()
    
    def __repr__(self):
        return f"Employee(id={self.id!r}, name='{self.full_name!r}', post='{self.post!r}')"