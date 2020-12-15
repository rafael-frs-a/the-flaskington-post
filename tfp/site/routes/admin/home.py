from flask import Blueprint, redirect, url_for

admin_home_route = Blueprint('admin_home_route', __name__)


@admin_home_route.route('/admin')
def home():
    return redirect(url_for('admin_user_route.user'))
