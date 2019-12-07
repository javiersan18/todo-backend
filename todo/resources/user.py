from flask import request
from flask_restful import Resource, abort, reqparse

from todo.extensions import db
from todo.models.user import User
from todo.security import pwd_context


class User(Resource):
    def get(self):
        print(request.remote_addr)
        return {'hello': 'world'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help="New user's email address. Email must not already exist in the database.")
        parser.add_argument('username', type=str, help="New user's username. Username must not already exist in the database.")
        parser.add_argument('password', type=str, help="New user's password.")
        args = parser.parse_args()
        print(
            args['email'],
            args['username'],
            args['password'],
            type(args['password'])
        )
        user = User(
            email=args['email'],
            username=args['username'],
            password_hash=pwd_context.hash(args['password']),
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'user created'}