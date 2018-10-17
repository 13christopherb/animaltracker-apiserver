from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

"""Initialization and configuration"""
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/animals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)