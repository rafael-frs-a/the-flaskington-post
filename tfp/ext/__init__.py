from . import database, migrate, hashing, login_manager, mail, url_serializer, logger


def init_app(app):
    database.init_app(app)
    migrate.init_app(app)
    hashing.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    url_serializer.init_app(app)
    logger.init_app(app)
