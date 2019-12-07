"""This app.py is based on the cookiecutter-flask template at https://github.com/cookiecutter-flask/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/app.py"""

from flask import Flask

from todo.extensions import (
    api,
    migrate,
    db,
    ma,
)


def register_extensions(app):
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    return None


def create_app(config_object="todo.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    return app


from todo.resources.user import UserResource
api.add_resource(UserResource, '/user')

if __name__ == '__main__':
    create_app().run(debug=True)