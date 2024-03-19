from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, create_refresh_token, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import UserModel, TrainingModel
from schemas import UsersSchema, UserDeleteTrainingSchema, TrainingUpdateSchema
from passlib.hash import pbkdf2_sha256
from blacklist import BLACKLIST


blueprint = Blueprint("users", __name__, description="Operations on users")


@blueprint.route('/users/<user_id>')
class User(MethodView):
    @jwt_required()
    @blueprint.response(200, UsersSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User removed"}


@blueprint.route('/users')
class UserList(MethodView):
    @jwt_required()
    @blueprint.response(200, UsersSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blueprint.route('/register')
class UserRegister(MethodView):
    @blueprint.arguments(UsersSchema)
    def post(self, new_user):
        user = UserModel(username=new_user["username"],
                         password=pbkdf2_sha256.hash(new_user["password"]))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting user")

        return {"message": "User registered successfully"}, 201


@blueprint.route('/login')
class UserLogin(MethodView):
    @blueprint.arguments(UsersSchema)
    def post(self, user_data):
        try:
            user = UserModel.query.filter_by(username=user_data["username"]).first_or_404()
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                # fresh is used to indicate the original access token
                # will be used to identify the token for action that are serious
                # like delete something from db
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            else:
                abort(401, message="Invalid credentials")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting user")


@blueprint.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logout"}, 200


@blueprint.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"access_token": new_token}, 200


@blueprint.route('/users_del_tr/<user_id>')
class UserDeleteTraining(MethodView):
    # with fresh, we indicate that we want to make this operation only with the original token
    @jwt_required(fresh=True)
    @blueprint.arguments(UserDeleteTrainingSchema)
    def delete(self, del_training, user_id):

        try:
            # based on the user id, day and time take the training
            training = TrainingModel.query.filter_by(day=del_training['day'],
                                                     time=del_training['time'],
                                                     user_id=user_id).first_or_404()
            # take the first value, which is the only value
            # and remove it
            if training:
                db.session.delete(training)
                db.session.commit()
            else:
                abort(404, message="the specified user does not have this training you are trying to remove")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting user")

        return {"message": "training removed"}


@blueprint.route('/user_update_tr/<user_id>')
class UserUpdateTraining(MethodView):
    @jwt_required(fresh=True)
    @blueprint.arguments(TrainingUpdateSchema)
    @blueprint.response(200, TrainingUpdateSchema)
    def put(self, new_training, user_id):
        try:
            # take from url params the day and the time of the specific user training
            url_args = request.args.to_dict()
            # search for it and try to update it
            training = TrainingModel.query.filter_by(day=url_args["day"],
                                                     time=url_args["time"],
                                                     user_id=user_id).first_or_404()
            if training:
                training.day = new_training.get("day", training.day)
                training.time = new_training.get("time", training.time)
                db.session.add(training)
                db.session.commit()
            else:
                abort(404, message="the specified user does not have this training you are trying to update")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting user")

        return training
