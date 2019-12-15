from flask import request, jsonify, make_response
from flask_restful import Resource, abort, reqparse
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

from todo.extensions import db
from todo.models.user import UserModel
from todo.security import pwd_context


class UserModelSchema(ModelSchema):
    """Marshmallow model schema to deserialize User object to dict."""
    class Meta:
        model = UserModel
        exclude = ('password_hash',)


class UserCreateSchema(Schema):
    """Marshmallow schema to validate incoming request data."""
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class UserPutSchema(Schema):
    """Marshmallow schema to validate incoming request update data."""
    email = fields.Email()
    username = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class UserResource(Resource):
    @staticmethod
    def _make_get_user_response(user):
        if not user:
            return make_response(jsonify({'message': 'user not found'}), 404)
        return UserModelSchema().dump(user)

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
                collection.append(UserModelSchema().dump(user))
            return make_response(jsonify(collection), 200)

    def post(self):
        args = request.get_json()
        try:
            UserCreateSchema().load(args)
            user = UserModel(
                email=args.get('email'),
                username=args.get('username'),
                first_name=args.get('first_name'),
                last_name=args.get('last_name'),
                password_hash=pwd_context.hash(args.get('password')),
            )
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                return make_response(jsonify({'message': e.__repr__()}), 400)
            return make_response(jsonify({'message': 'user created'}), 201)
        except Exception as e:
            return make_response(jsonify({'message': e.messages}), 400)

    def put(self, user_id=None, username=None):
        args = request.get_json()
        if not args:
            return make_response(jsonify({'message': 'Missing JSON request body'}), 400)
        try:
            UserPutSchema().load(args)
            if not user_id and not username:
                return make_response(jsonify({'message': 'User ID or username not specified in URL path'}), 400)
            if user_id:
                user = UserModel.query.filter_by(id=user_id).first()
                for key in args:
                    setattr(user, key, args[key])
                db.session.commit()
            elif username:
                user = UserModel.query.filter_by(username=username).first()
                for key in args:
                    setattr(user, key, args[key])
                db.session.commit()
        except Exception as e:
            return make_response(jsonify({'message': e.__repr__()}), 400)
        return make_response(jsonify({'message': 'user updated'}), 200)

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