from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

"""Initialization and configuration"""
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jdjrchsjifapjp:cad088a14a2dd90e75b3ae71f13bfa4a43c154e70257bd5fd42b800542c17c60@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dadelfp0dkv1uc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)