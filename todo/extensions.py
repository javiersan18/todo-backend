from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

api = Api()
migrate = Migrate()
db = SQLAlchemy()