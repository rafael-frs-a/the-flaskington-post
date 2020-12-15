from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import current_user

errors_route = Blueprint('errors_route', __name__)


@errors_route.app_errorhandler(405)
def error_405(error):
    return render_template('errors/405.html', title='Method Not Allowed'), 405


@errors_route.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Page Not Found'), 404


@errors_route.app_errorhandler(403)
def error_403(error):
    if not current_user.is_authenticated:
        return redirect(url_for('login_route.login'))

    return render_template('errors/403.html', title='Forbidden'), 403


@errors_route.app_errorhandler(401)
def error_401(error):
    if not current_user.is_authenticated:
        session['login-redirect'] = request.url
        return redirect(url_for('login_route.login'))

    return render_template('errors/401.html', title='Unauthorized'), 401
