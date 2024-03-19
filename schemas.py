from marshmallow import Schema, fields


class PlainTrainingSchema(Schema):
    # id = fields.Str(dump_only=True)
    day = fields.Str(required=True)
    time = fields.Str(required=True)


class PlainUsersSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class TrainingSchema(PlainTrainingSchema):
    user_id = fields.Str(required=True)
    # user = fields.Nested(PlainUsersSchema(), dump_only=True)


class TrainingUpdateSchema(Schema):
    day = fields.Str()
    time = fields.Str()


class UsersSchema(PlainUsersSchema):
    trainings = fields.List(fields.Nested(PlainTrainingSchema()), dump_only=True)


class UserDeleteTrainingSchema(Schema):
    day = fields.Str()
    time = fields.Str()
