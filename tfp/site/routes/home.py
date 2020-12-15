from flask import Blueprint
from .post import home_posts

home_route = Blueprint('home_route', __name__)


@home_route.route('/')
def home():
    return home_posts()
