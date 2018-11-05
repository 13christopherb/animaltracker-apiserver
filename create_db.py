from models import db, LocationModel

if __name__ == '__main__':
    db.create_all()
    nro = LocationModel(location_name='NRO')
    mbo = LocationModel(location_name='MBO')
    slo = LocationModel(location_name='SLO')
    nro.save_to_db()
    mbo.save_to_db()
    slo.save_to_db()