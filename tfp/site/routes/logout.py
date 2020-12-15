from functools import wraps
from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user, current_user

logout_route = Blueprint('logout_route', __name__)


def logout_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            flash(
                'This action cannot be completed while you are logged in. Please, logout first.', 'warning')
            return redirect(url_for('home_route.home'))

        return func(*args, **kwargs)

    return decorated


@logout_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_route.home'))
