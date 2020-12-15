from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from tfp.ext.database import db
from tfp.services.email_sender import email_sender
from tfp.site.models.user import User, Role, get_users, get_rand_id
from tfp.site.models.email import Email
from tfp.site.forms.admin.user_form import AdminNewUserForm, AdminEditUserForm
from ..register import send_confirmation_email
from ..account import send_delete_request_email

admin_user_route = Blueprint('admin_user_route', __name__)


def send_banishment_email(user, reason):
    msg = render_template(
        'banishment_alert.html', name=user.name, reason=reason)

    email = Email(subject='Banishment Alert', body=msg, recipient=user)
    db.session.add(email)
    db.session.commit()
    email_sender.set()


def feed_role_choices(form):
    roles = Role.query.all()
    form.roles.choices = [(_.name, _.name) for _ in roles]


@admin_user_route.route('/admin/user')
def user():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    desc = request.args.get('desc')
    per_page = 10

    if sort:
        users = get_users(per_page, page, sort, desc)
    else:
        users = get_users(per_page, page, 'created_at', True)

    return render_template('admin/user.html', title='User', users=users)


def route_user_form(user):
    if user:
        cls_form = AdminEditUserForm
        template = 'admin/user_form_edit.html'
        title = user.username
    else:
        cls_form = AdminNewUserForm
        template = 'admin/user_form_new.html'
        title = 'User'

    try:
        form_data = session.pop('user-form-data')
        form_errors = session.pop('user-form-errors')
    except KeyError:
        form = cls_form()
        feed_role_choices(form)

        if cls_form is AdminEditUserForm:
            form.roles.data = user.roles_names
            form.banned.data = user.banned
            form.delete_request.data = user.delete_request
            form.current_user = user

        return render_template(template, title=title,
                               form=form, url_back=url_for('admin_user_route.user'))

    form = cls_form(data=form_data)
    feed_role_choices(form)
    return render_template(template, title=title, form=form,
                           errors=form_errors, url_back=url_for('admin_user_route.user'), user=user)


@admin_user_route.route('/admin/user/new', methods=['GET'])
def new_user():
    return route_user_form(None)


@admin_user_route.route('/admin/user/new', methods=['POST'])
def new_user_prg():
    form = AdminNewUserForm()
    feed_role_choices(form)

    if form.validate_on_submit():
        user = User(name=form.name.data, user_email=form.email.data,
                    password=form.password.data, roles_names=form.roles.data)
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(user)
        return redirect(url_for('admin_user_route.user'))

    session['user-form-data'] = form.data
    session['user-form-errors'] = form.errors
    return redirect(url_for('admin_user_route.new_user'))


@admin_user_route.route('/admin/user/<username>', methods=['GET'])
def edit_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return route_user_form(user)


@admin_user_route.route('/admin/user/<username>', methods=['POST'])
def edit_user_prg(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AdminEditUserForm()
    feed_role_choices(form)
    form.current_user = user

    if form.validate_on_submit():
        previous_delete_request = user.delete_request
        previous_banned = user.banned
        user.roles_names = form.roles.data
        user.banned = form.banned.data
        user.delete_request = form.delete_request.data

        if user.banned and user.banned != previous_banned:
            user.login_id = get_rand_id()
            user.delete_profile_picture()
            send_banishment_email(user, form.ban_reason.data)

        db.session.commit()

        if user.delete_request and user.delete_request != previous_delete_request:
            send_delete_request_email(user)

        return redirect(url_for('admin_user_route.user'))

    session['user-form-data'] = form.data
    session['user-form-errors'] = form.errors
    return redirect(url_for('admin_user_route.edit_user', username=username))


@admin_user_route.route('/admin/user/delete/<username>', methods=['POST'])
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    user.delete_request = datetime.utcnow()
    db.session.commit()
    send_delete_request_email(user)
    return redirect(request.referrer if request.referrer else url_for('admin_user_route.user'))
