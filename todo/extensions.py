from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS

from todo.settings import FLASK_ADMIN_NAME, FLASK_ADMIN_TEMPLATE_MODE

api = Api()
migrate = Migrate()
db = SQLAlchemy()
ma = Marshmallow()
admin = Admin(name=FLASK_ADMIN_NAME, template_mode=FLASK_ADMIN_TEMPLATE_MODE)
cors = CORS(resources={r"/*": {"origins": "*"}})