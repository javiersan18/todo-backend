from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

api = Api()
migrate = Migrate()
db = SQLAlchemy()
ma = Marshmallow()