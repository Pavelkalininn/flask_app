from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)

    def __init__(self, name, username):
        self.name = name
        self.username = username

    def json(self):
        return {"name": self.name, "username": self.username}


class ParametersModel(db.Model):
    __tablename__ = 'parameters'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), db.ForeignKey('users.username'))
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    value = db.Column(db.String(80))
    __table_args__ = (UniqueConstraint('user', 'name', 'type',
                                       name='_user_name_type_unique'),
                      )

    def __init__(self, user, name, type, value):
        self.user = user
        self.name = name
        self.type = type
        self.value = value

    def json(self):
        return {
            "user": self.user,
            "name": self.name,
            "type": self.type,
            "value": self.value
        }
