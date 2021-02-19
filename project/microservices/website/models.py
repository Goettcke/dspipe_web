from flask_login import UserMixin
from sqlalchemy import ForeignKey
from . import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(200), nullable=False)
    q_measure = db.Column(db.String(200), nullable=False)
    dataset_name = db.Column(db.String(200), nullable=False)
    per = db.Column(db.Integer, nullable=False)
    number_of_samples = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    parameters = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id", ondelete="CASCADE"))


    def __repr__(self):
        return f"-----Task-----\nalgorithm: {self.algorithm}\ndataset: {self.dataset_name}\nq_measure: {self.q_measure}\n per: {self.per}\n ns:{self.number_of_samples}\n id:{self.user_id}"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_type = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class ResultCatalog(db.Model):
    result_id = db.Column(db.Integer, nullable=False, primary_key=True)
    algorithm = db.Column(db.String(30), nullable=False)


class UserResult(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    result_id = db.Column(db.Integer, ForeignKey("result_catalog.result_id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

