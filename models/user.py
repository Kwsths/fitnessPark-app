from db import db
from sqlalchemy import Integer, Column, String


class UserModel(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    # first arg: the class on which we have the relationship, back_populates: the column of the model with the relationship
    trainings = db.relationship('TrainingModel', back_populates="user", lazy='dynamic', cascade='all, delete')

