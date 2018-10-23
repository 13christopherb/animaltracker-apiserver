from __init__ import db
from passlib.hash import pbkdf2_sha256 as sha256


class AnimalModel(db.Model):
    """Represents an item in an inventory"""

    """Represents an item in an inventory"""
    __tablename__ = 'animal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    species = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer)
    isGettingTubed = db.Column(db.Boolean)
    isGettingControlledMeds = db.Column(db.Boolean)
    location = db.Column(db.String(3), nullable=False)


    @property
    def serialize(self):
        """
        Serializes the Item to a JSON object

        :return: JSON representation of the item
        """

        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'weight': self.weight,
            'isGettingTubed': self.isGettingTubed,
            'isGettingControlledMeds': self.isGettingControlledMeds,
            'location': self.location
        }


class TransportModel(db.Model):
    __tablename__ = 'transport'
    id = db.Column(db.Integer, primary_key=True)
    departs = db.Column(db.String(3), nullable=False)
    arrives = db.Column(db.String(3), nullable=False)
    meetTime = db.Column(db.DateTime(), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    animal = db.relationship('AnimalModel',
                               backref=db.backref('transport', lazy=True))

    def add_animal(self, animal):
        """
        Adds a animal to the transport's list of categories

        :param animal: The animal to be added
        """

        self.animal.append(animal)
        return self

    def remove_category(self, animal):
        if len(self.animal) > 1:
            self.animal.remove(animal)
            return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
