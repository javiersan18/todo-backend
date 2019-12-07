from datetime import datetime

from todo.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)