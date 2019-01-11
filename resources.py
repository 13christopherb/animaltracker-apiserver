from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from schemas import animal_schema, animals_schema, location_schema, locations_schema, \
    transport_schema, transports_schema
from models import AnimalModel, LocationModel, UserModel, TransportModel, RevokedTokenModel, db
from __init__ import jwt

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

transport_parser = reqparse.RequestParser()
transport_parser.add_argument('departs', help='This field cannot be blank', required=True)
transport_parser.add_argument('arrives', help='This field cannot be blank', required=True)
transport_parser.add_argument('meetTime', help='This field cannot be blank', required=True)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The token has expired'
    }), 401


class Animals(Resource):
    @jwt_required
    def get(self):
        obj = AnimalModel.query.all()
        result = animals_schema.dump(obj)
        animals = {'animals': result.data}
        return animals

    @jwt_required
    def post(self):
        data = request.get_json()
        new_animal = animal_schema.load(data).data
        location = LocationModel.query.filter_by(name=data['location']).one_or_none()
        try:
            location.add_animal(new_animal)
            location.save_to_db()
            result = animal_schema.dump(new_animal)
            return jsonify({'animal': result.data})
        except:
            return {'message': 'Something went wrong'}, 500


class Animal(Resource):
    @jwt_required
    def post(self, animal_id):
        data = request.get_json()
        obj = AnimalModel.query.filter_by(id=animal_id).one_or_none()
        old_animal = animal_schema.dump(obj)
        obj.name = data['location']
        result = animal_schema.dump(obj)
        try:
            obj.save_to_db()
            return jsonify({
                'old': old_animal.data,
                'new': result.data
            })
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self, animal_id):
        obj = AnimalModel.query.filter_by(id=animal_id).one_or_none()
        db.session.delete(obj)
        db.session.commit()
        return 200


class Location(Resource):
    @jwt_required
    def get(self, name):
        obj = LocationModel.query.filter_by(name=name).one_or_none()
        result = locations_schema.dump(obj)
        location = {'location': result.data}
        return location

    @jwt_required
    def post(self, name):
        data = request.get_json()
        obj = LocationModel.query.filter_by(name=name).one_or_none()
        old_location = location_schema.dump(obj)
        obj.last_updated = data['lastUpdated']
        result = animal_schema.dump(obj)
        try:
            obj.save_to_db()
            return jsonify({
                'old': old_location.data,
                'new': result.data
            })
        except:
            return {'message': 'Something went wrong'}, 500


class Locations(Resource):
    @jwt_required
    def get(self):
        obj = LocationModel.query.all()
        result = locations_schema.dump(obj)
        return {'locations': result.data}


class Transport(Resource):
    @jwt_required
    def get(self, transport_id):
        obj = TransportModel.query.all()
        result = transports_schema.dump(obj)
        transports = {'transports': result.data}
        return jsonify(transports)

    @jwt_required
    def delete(self, transport_id):
        obj = TransportModel.query.filter_by(id=transport_id).one_or_none()
        db.session.delete(obj)
        db.session.commit()
        return ''


class TransportList(Resource):
    @jwt_required
    def get(self):
        obj = TransportModel.query.all()
        result = transports_schema.dump(obj)
        print(result)
        transports = {'transports': result.data}
        return jsonify(transports)

    @jwt_required
    def post(self):
        data = request.get_json()
        new_transport = transport_schema.load(data).data
        try:
            new_transport.save_to_db()
            result = transport_schema.dump(new_transport)
            return jsonify(result.data)
        except:
            return {'message': 'Something went wrong'}, 500


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            location=data['location']
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
            return {'message': 'User {} doesn\'t exist'.format(data['username'])},401

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
            return {'message': 'Wrong credentials'},401


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
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'accessToken': access_token}


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
