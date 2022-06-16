from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    ishead=db.Column(db.Boolean(), default=False, nullable=False)

class Data(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(1000)) # primary keys are required by SQLAlchemy
    district = db.Column(db.String(1000))
    sub_district = db.Column(db.String(100))
    panchayat = db.Column(db.String(1000))
    no_audit = db.Column(db.Integer)
    name = db.Column(db.String(1000))