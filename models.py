from flask_sqlalchemy import SQLAlchemy
from __init__ import db


class Animal(db.Model):
    """Represents an item in an inventory"""

    """Represents an item in an inventory"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    species = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer)
    isGettingTubed = db.Column(db.Boolean)
    isGettingControlledMeds = db.Column(db.Boolean)

    @property
    def serialize(self):
        """
        Serializes the Item to a JSON object

        :return: JSON representation of the item
        """

        return {
            'id':       self.id,
            'name':     self.name,
            'species':      self.species,
            'weight':     self.weight,
            'isGettingTubed': self.isGettingTubed,
            'isGettingControlledMeds': self.isGettingControlledMeds
        }