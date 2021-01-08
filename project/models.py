from flask_login import UserMixin
from . import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(200), nullable=False)
    per_un = db.Column(db.Integer, nullable=False)
    number_of_samples = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # This user id should be setup 
    #user_id = db.Column(db.integer, models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE))

    def __repr__(self):
        return f"<Task {self.dataset_name}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
