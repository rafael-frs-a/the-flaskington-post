from flask import Blueprint, session, render_template, redirect, url_for, flash, request
from flask_login import login_user
from tfp.site.forms.login_form import LoginForm
from tfp.site.models.user import User
from .logout import logout_required

login_route = Blueprint('login_route', __name__)


def use_url_login_redirect(url):
    blacklist_routes = ['login', 'register', 'logout',
                        'confirm-account', 'recover-account']

    for route in blacklist_routes:
        if url.startswith(request.url_root + route):
            return False

    return True


@login_route.route('/login', methods=['GET'])
@logout_required
def login():
    if request.referrer and use_url_login_redirect(request.referrer):
        session['login-redirect'] = request.referrer

    try:
        form_data = session.pop('login-form-data')
        form_errors = session.pop('login-form-errors')
    except KeyError:
        return render_template('login.html', title='Log In', form=LoginForm())

    return render_template('login.html', title='Log In', form=LoginForm(data=form_data), errors=form_errors)


@login_route.route('/login', methods=['POST'])
@logout_required
def login_prg():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            user = User.query.filter_by(username=form.email.data).first()

        if (user and user.password_match(form.password.data) and
                user.confirmed_at and not user.banned):
            login_user(user)

            try:
                url = session.pop('login-redirect')
                return redirect(url)
            except KeyError:
                return redirect(url_for('home_route.home'))
        else:
            flash('Login failed. Please verify your email and password.', 'danger')

    session['login-form-data'] = form.data
    session['login-form-errors'] = form.errors
    return redirect(url_for('login_route.login'))
