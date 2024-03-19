from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import TrainingModel, UserModel
from schemas import TrainingSchema, TrainingUpdateSchema
from db import db

blueprint = Blueprint("trainings", __name__, description="operations on trainings")


@blueprint.route('/training/<training_id>')
class Training(MethodView):
    @jwt_required()
    @blueprint.response(200, TrainingSchema)
    def get(self, training_id):
        training = TrainingModel.query.get_or_404(training_id)
        return training


@blueprint.route('/trainings')
class TrainingsList(MethodView):
    @jwt_required()
    @blueprint.response(200, TrainingSchema(many=True))
    def get(self):
        return TrainingModel.query.all()

    @jwt_required()
    @blueprint.arguments(TrainingSchema)
    @blueprint.response(200, TrainingSchema)
    def post(self, new_training):
        training = TrainingModel(**new_training)
        print(training.user_id)
        print(new_training)
        try:
            # if user does not exist do not add training
            UserModel.query.get_or_404(training.user_id)
            db.session.add(training)
            db.session.commit()
        except IntegrityError:
            abort(400, message="This user has already this training")
        except SQLAlchemyError:
            abort(500, message="An error eccured while inserting training")

        return training
