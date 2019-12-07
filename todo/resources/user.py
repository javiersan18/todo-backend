from flask import request
from flask_restful import Resource, abort, reqparse

from todo.extensions import db, ma
from todo.models.user import UserModel
from todo.security import pwd_context


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'username', 'created_at')


class UserResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help="A user's username.")
        args = parser.parse_args()
        user = UserModel.query.filter_by(username=args['username']).first()
        return UserSchema().dump(user)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help="New user's email address. Email must not already exist in the database.")
        parser.add_argument('username', type=str, help="New user's username. Username must not already exist in the database.")
        parser.add_argument('password', type=str, help="New user's password.")
        args = parser.parse_args()

        user = UserModel(
            email=args['email'],
            username=args['username'],
            password_hash=pwd_context.hash(args['password']),
        )

        db.session.add(user)
        db.session.commit()
        return {'message': 'user created'}