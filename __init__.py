from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

"""Initialization and configuration"""
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/animals'
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://postgresql-graceful-65901'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True
heroku = Heroku(app)
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

jwt._set_error_handler_callbacks(api)




