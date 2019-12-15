"""This app.py is based on the cookiecutter-flask template at https://github.com/cookiecutter-flask/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/app.py"""

from flask import Flask
from flask_admin.contrib.sqla import ModelView

from todo.extensions import (
    api,
    migrate,
    db,
    ma,
    admin,
    cors,
)


def register_extensions(app):
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    admin.init_app(app)
    cors.init_app(app)

    return None


def create_app(config_object="todo.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    return app

# Register Flask-Restful API view endpoints.
from todo.resources.user import UserResource
api.add_resource(
    UserResource,
    '/user',
    '/user/<int:user_id>',
    '/user/<string:username>',
)

# Register Flask-Admin views
# TODO: Add security for admin panel.
from todo.models.user import UserModel
admin.add_view(ModelView(UserModel, db.session))

if __name__ == '__main__':
    create_app().run(debug=True)