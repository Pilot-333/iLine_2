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
    manager = relationship("Employee", remote_side=[id], backref="subordinates") # Определение отношения "многие-к-одному" (подчинённые -> начальник)
    
    def __repr__(self):
        return f"Employee(id={self.id!r}, name='{self.full_name!r}', post='{self.post!r}')"