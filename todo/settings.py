from os import environ

SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'postgres://postgres:ROOT@localhost:5432/bioflask')
FLASK_ADMIN_NAME = environ.get('FLASK_ADMIN_NAME', 'Todo Admin Panel')
FLASK_ADMIN_TEMPLATE_MODE = environ.get('FLASK_ADMIN_TEMPLATE_MODE', 'bootstrap3')
SECRET_KEY = environ.get('SECRET_KEY', 'a-very-bad-secret-key')