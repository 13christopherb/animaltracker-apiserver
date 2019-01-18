from models import db, LocationModel, UserModel

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    nro = LocationModel(name='NRO')
    mbo = LocationModel(name='MBO')
    slo = LocationModel(name='SLO')
    nro.save_to_db()
    mbo.save_to_db()
    slo.save_to_db()
    new_user = UserModel(
        username='username',
        password=UserModel.generate_hash('password'),
        location='loc'
    )
    new_user.save_to_db()