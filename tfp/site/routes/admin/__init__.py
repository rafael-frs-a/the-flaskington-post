from flask import abort
from flask_login import login_required, current_user
from .home import admin_home_route
from .user import admin_user_route
from .role import admin_role_route
from .post import admin_post_route
from .email import admin_email_route


def init_app(app):
    @login_required
    def admin_required():
        if not current_user.has_role('admin'):
            abort(403)

    def register_blueprint(bp):
        bp.before_request(admin_required)
        app.register_blueprint(bp)

    register_blueprint(admin_home_route)
    register_blueprint(admin_user_route)
    register_blueprint(admin_role_route)
    register_blueprint(admin_post_route)
    register_blueprint(admin_email_route)
