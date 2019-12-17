from flask import request, jsonify, make_response
from flask_restful import Resource, abort, reqparse
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

from todo.extensions import db
from todo.models.user import UserModel
from todo.security import pwd_context

import datetime


class UserModelSchema(ModelSchema):
    """Marshmallow model schema to deserialize User object to dict."""
    class Meta:
        model = UserModel
        exclude = ('password',)


class UserCreateSchema(Schema):
    """Marshmallow schema to validate incoming request data."""
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    surname1 = fields.Str(required=True)
    surname2 = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class UserPutSchema(Schema):
    """Marshmallow schema to validate incoming request update data."""
    email = fields.Email()
    password = fields.Str()
    name = fields.Str()
    surname1 = fields.Str()
    surname2 = fields.Str()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()


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
            user = UserModel(args)
            try:
                user.save()
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
                user.update(args)
            elif username:
                user = UserModel.query.filter_by(username=username).first()
                user.update(args)
        except Exception as e:
            return make_response(jsonify({'message': e.__repr__()}), 400)
        return make_response(jsonify({'message': 'user updated'}), 200)

    def delete(self, user_id=None, username=None):
        if not user_id and not username:
            return make_response(jsonify({'message': 'User ID or username not specified in URL path'}), 400)

        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            user.delete()
        elif username:
            user = UserModel.query.filter_by(username=username).first()
            user.delete()
        return make_response(jsonify({'message': 'User has been deleted'}), 200)