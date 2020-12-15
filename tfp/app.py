from flask import Flask
from .ext import config


def create_app():
    app = Flask(__name__)
    config.load_config(app)
    config.load_extensions(app)
    return app
