import os


def allowed_attributes(tag, name, value):
    return True


class Config:
    APP_NAME = 'The Flaskington Post'

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = (APP_NAME,
                           os.getenv('MAIL_USERNAME'))
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_MAX_EMAILS = 50
    MAIL_SEND_INTERVAL = 60  # 1 minute

    DELETE_USERS_INTERVAL = 60 * 5  # 5 minutes
    ACCOUNT_DELETE_INTERVAL = 48  # 48 hours

    ALLOWED_PROFILE_PICS = ['jpg', 'jpeg', 'png']
    ALLOWED_POST_TAGS = [
        'html', 'head', 'title', 'body',
        'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote',
        'pre', 'b', 'u', 'i', 'strong', 'em', 'strike', 'sub', 'sup',
        'img', 'span', 'ul', 'ol', 'li', 'a', 'div'
    ]

    ALLOWED_POST_ATTRIBUTES = allowed_attributes
    ALLOWED_POST_STYLES = ['color', 'background-color',
                           'text-align', 'height', 'width']

    EXTENSIONS = [
        'tfp.ext',
        'tfp.cli.commands',
        'tfp.site.routes',
        'tfp.services'
    ]
