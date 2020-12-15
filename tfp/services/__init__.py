from .email_sender import init_email_sender
from .user_deleter import init_user_deleter


def init_app(app):
    init_email_sender(app)
    init_user_deleter(app)
