from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.user import blueprint as UserBluePrint
from resources.training import blueprint as TrainingBluePrint
from db import db
from blacklist import BLACKLIST
import os
import models # will call from init of module all models

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Fitness Park Rest Api"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/nmp/swagger-ui-dist/"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///calendar.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has been revoked", "error": "Token revoked"}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The provided token is expired", "error": "token expired"}), 401


@jwt.invalid_token_loader
def invalid_token_loader_callback(error):
    return jsonify({"message": "Signature verification failed", "error": "invalid token"}), 401


# handle cases that tries to access endpoints without a token
@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify({"message": "Request does not contain a token", "error": "authorization required"}), 401


# handle cases that use a not fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token is not fresh", "error": "Fresh token required"}), 401


db.init_app(app)

api = Api(app)

with app.app_context():
    db.create_all()

api.register_blueprint(UserBluePrint)
api.register_blueprint(TrainingBluePrint)

if __name__ == "__main__":
    app.run(debug=True)