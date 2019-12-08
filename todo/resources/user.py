from flask import request, jsonify, make_response
from flask_restful import Resource, abort, reqparse
from marshmallow_sqlalchemy import ModelSchema

from todo.extensions import db
from todo.models.user import UserModel
from todo.security import pwd_context


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        exclude = ('password_hash',)


class UserResource(Resource):
    @staticmethod
    def _make_get_user_response(user):
        if not user:
            return make_response(jsonify({'message': 'user not found'}), 404)
        return UserSchema().dump(user)

    def get(self, user_id=None, username=None):
        # Get user by id or username.
        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            return UserResource._make_get_user_response(user)
        elif username:
            user = UserModel.query.filter_by(username=username).first()
            return UserResource._make_get_user_response(user)

        # Get a collection of users.
        else:
            users = UserModel().query.all()
            collection = []
            for user in users:
                collection.append(UserSchema().dump(user))
            return make_response(jsonify(collection), 200)

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

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'message': e.__repr__()}), 400)
        return make_response(jsonify({'message': 'user created'}), 201)

    def delete(self, user_id=None, username=None):
        if not user_id and not username:
            return make_response(jsonify({'message': 'User ID or username not specified in URL path'}), 400)

        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
        elif username:
            user = UserModel.query.filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
        return make_response(jsonify({'message': 'User has been deleted'}), 200)