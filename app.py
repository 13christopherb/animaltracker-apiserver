from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from __init__ import app, db
from models import Animal


CORS(app, resources={r"/*": {"origins": "*"}})
ma = Marshmallow(app)


class AnimalSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'species', 'weight', 'isGettingTubed', 'isGettingControlledMeds', 'id')


animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)



@app.route('/')
def index():
    return "index"

# API


@app.route('/animals', methods=['GET','POST', 'OPTIONS'])
def animals():
    """
    Returns a json object representing an item

    :return: json representation of item
    """
    if request.method == 'GET':
        obj = Animal.query.all()
        result = animals_schema.dump(obj)
        test = {'animals': result.data}
        print(result.data)
        return jsonify(test)

    if request.method == 'POST':
        obj = request.get_json()
        animal = Animal(name=obj['name'], species=obj['species'], weight=obj['weight'],
                        isGettingTubed=obj['isGettingTubed'],
                        isGettingControlledMeds=obj['isGettingControlledMeds'])

        db.session.add(animal)
        db.session.commit()
        #response = request.get_json()
        return jsonify(animal.serialize)

    obj = 'test'
    return jsonify(obj)


@app.route('/animals/<animal_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
def animal(animal_id):
    if request.method == 'DELETE':
        obj = Animal.query.filter_by(id=animal_id).one_or_none()
        db.session.delete(obj)
        db.session.commit()
    return '500'

if __name__ == '__main__':
    db.init_app(app)
    db.app = app
    app.debug = True
    app.run(host='0.0.0.0', port=5000)