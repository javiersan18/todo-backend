from datetime import datetime

from todo.extensions import db

from todo.security import pwd_context


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name1 = db.Column(db.String(128), nullable=False)
    last_name2 = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        """
            Class constructor
        """
        self.username = data.get('username'),
        self.email = data.get('email'),
        self.password = pwd_context.hash(data.get('password')),
        self.name = data.get('name'),
        self.surname1 = data.get('surname1'),
        self.surname2 = data.get('surname2'),
        self.created_at = datetime.datetime.utcnow(),
        self.modified_at = datetime.datetime.utcnow(),

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':  # add this new line
                self.password = pwd_context.hash(item)  # add this new line
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)
