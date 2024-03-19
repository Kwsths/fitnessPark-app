from db import db
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey


class TrainingModel(db.Model):
    __tablename__ = 'training'
    # id = Column(Integer, primary_key=True)
    day = Column(String(80), primary_key=True, unique=False, nullable=False)
    time = Column(String(10), primary_key=True, unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="trainings")
