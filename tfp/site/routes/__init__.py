from .home import home_route
from .login import login_route
from .register import register_route
from .account_confirm import account_confirm_route
from .logout import logout_route
from .account import account_route
from .recover_account import recover_account_route
from .post import posts_route
from .errors import errors_route
from . import admin


def init_app(app):
    app.register_blueprint(home_route)
    app.register_blueprint(account_route)
    app.register_blueprint(account_confirm_route)
    app.register_blueprint(login_route)
    app.register_blueprint(register_route)
    app.register_blueprint(logout_route)
    app.register_blueprint(recover_account_route)
    app.register_blueprint(posts_route)
    app.register_blueprint(errors_route)
    admin.init_app(app)
