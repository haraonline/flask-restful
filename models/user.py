from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):  # id is not required here is inserted and as auto-increment
        # the following should match the db column names
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):  # cls refers to the current class name
        return cls.query.filter_by(username=username).first()  # db.username = argument.username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()  # id is from database, _id is the argument
