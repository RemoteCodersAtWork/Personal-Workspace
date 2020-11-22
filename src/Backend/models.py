from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, force_auto_coercion, ScalarListType
from sqlalchemy import DateTime

ma = Marshmallow()
db = SQLAlchemy()

class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key = True)
    firstname = db.Column(db.String(20), unique = False, nullable = False)
    lastname = db.Column(db.String(20), unique = False, nullable = False)
    number = db.Column(db.String(12), unique = True, nullable = False)
    email = db.Column(EmailType(), unique=True, nullable = False)
    password = db.Column(db.String)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    
    def __init__(self, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.number = number
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<id {}>'.format(self, id)

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'number': self.number,
            'email': self.email,
            'password': self.password
        }