from marshmallow import fields, post_load, pre_load
from flask_marshmallow import Marshmallow
from __init__ import ma
from models import AnimalModel, LocationModel, TransportModel


class AnimalSchema(ma.Schema):
    name = fields.String()
    species = fields.String()
    weight = fields.String()
    isGettingTubed = fields.Boolean(attribute='is_getting_tubed')
    isGettingControlledMeds = fields.Boolean(attribute='is_getting_controlled_meds')
    location = fields.String(attribute='location')
    id = fields.Integer(dump_only=True)
    timestamp = fields.DateTime()

    @post_load
    def make_animal(self, data):
        return AnimalModel(**data)


class LocationSchema(ma.Schema):
    name = fields.String(attribute='name')
    animals = fields.Nested(AnimalSchema, many=True)
    lastUpdated = fields.DateTime(attribute='last_updated')

    @post_load
    def make_location(self, data):
        return LocationModel(**data)


class TransportSchema(ma.Schema):
    meetTime = fields.DateTime(attribute='meet_time')
    meetPlace = fields.String(attribute='meet_place')
    departs = fields.String()
    arrives = fields.String()
    id = fields.Integer(dump_only=True)

    @post_load
    def make_transport(self, data):
        return TransportModel(**data)


animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
transport_schema = TransportSchema()
transports_schema = TransportSchema(many=True)