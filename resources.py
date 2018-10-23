from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from __init__ import animals_schema, transports_schema
from models import AnimalModel, UserModel, TransportModel, RevokedTokenModel, db

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

transport_parser = reqparse.RequestParser()
transport_parser.add_argument('departs', help='This field cannot be blank', required=True)
transport_parser.add_argument('arrives', help='This field cannot be blank', required=True)
transport_parser.add_argument('meetTime', help='This field cannot be blank', required=True)


class Animals(Resource):
    def get(self):
        obj = AnimalModel.query.all()
        result = animals_schema.dump(obj)
        animals = {'animals': result.data}
        return animals

    def post(self):
        obj = request.get_json()
        animal = AnimalModel(name=obj['name'], species=obj['species'], weight=obj['weight'],
                             isGettingTubed=obj['isGettingTubed'],
                             isGettingControlledMeds=obj['isGettingControlledMeds'], location=obj['location'])

        db.session.add(animal)
        db.session.commit()
        return {'animal': animal.serialize}


class AnimalDeletion(Resource):
    def delete(self, animal_id):
        obj = AnimalModel.query.filter_by(id=animal_id).one_or_none()
        db.session.delete(obj)
        db.session.commit()
        return ''


class Transport(Resource):
    def get(self, transport_id):
        obj = TransportModel.query.all()
        result = transports_schema.dump(obj)
        transports = {'transports': result.data}
        return jsonify(transports)


class TransportList(Resource):
    def get(self):
        obj = TransportModel.query.all()
        result = transports_schema.dump(obj)
        transports = {'transports': result.data}
        return jsonify(transports)

    def post(self):
        data = transport_parser.parse_args()
        new_transport = TransportModel(
            departs=data['departs'],
            arrives=data['arrives'],
            meetTime=data['meetTime']
        )
        try:
            new_transport.save_to_db()
            return {
                'message': 'Transport {} was created'.format(data['meetTime']),
            }
        except:
            return {'message': 'Something went wrong'}, 500

class UserRegistration(Resource):
    def post(self):
        data = login_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'username': data['username']
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
