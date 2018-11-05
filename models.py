
from __init__ import db
from passlib.hash import pbkdf2_sha256 as sha256


class AnimalModel(db.Model):
    __tablename__ = 'animal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    species = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer)
    is_getting_tubed = db.Column(db.Boolean)
    is_getting_controlled_meds = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime(timezone=True))

    location_name = db.Column(db.String, db.ForeignKey('location.location_name'))
    location = db.relationship('LocationModel', backref=db.backref('animals'), lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class LocationModel(db.Model):
    __tablename__ = 'location'
    location_name = db.Column(db.String(3), primary_key=True)

    def add_animal(self, animal):
        self.animals.append(animal)
        return self

    def remove_animal(self, animal):
        if len(self.animal) > 1:
            self.animal.remove(animal)
            return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class TransportModel(db.Model):
    __tablename__ = 'transport'
    id = db.Column(db.Integer, primary_key=True)
    departs = db.Column(db.String(3), nullable=False)
    arrives = db.Column(db.String(3), nullable=False)
    meet_time = db.Column(db.DateTime(timezone=True), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    animal = db.relationship('AnimalModel',
                               backref=db.backref('transport', lazy=True))

    def add_animal(self, animal):
        self.animal.append(animal)
        return self

    def remove_animal(self, animal):
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