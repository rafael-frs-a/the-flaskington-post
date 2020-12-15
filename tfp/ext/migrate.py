from flask_migrate import Migrate
from tfp.site.models import *
from .database import db

migrate = Migrate()


def init_app(app):
    migrate.init_app(app, db)
