from flask_cors import CORS

from __init__ import app, db, api, jwt
import models
import resources



CORS(app, resources={r"/*": {"origins": "*"}})


api.add_resource(resources.Animals, '/animals')
api.add_resource(resources.Animal, '/animal/<string:animal_id>')
api.add_resource(resources.Locations, '/locations')
api.add_resource(resources.TransportList, '/transports')
api.add_resource(resources.Transport, '/transport/<string:transport_id>')
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@app.route('/')
def index():
    return "index"

if __name__ == '__main__':
    db.init_app(app)
    db.app = app
    app.debug = True
    app.run()