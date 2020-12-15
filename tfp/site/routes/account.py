import os
import secrets
from datetime import datetime
from flask import Blueprint, session, render_template, redirect, url_for, current_app, flash
from flask_login import current_user, login_required, logout_user
from PIL import Image
from tfp.ext.database import db
from tfp.ext.url_serializer import url_serializer
from tfp.services.email_sender import email_sender
from tfp.site.forms.account_form import UpdateAccountForm
from tfp.site.models.user import User
from tfp.site.models.email import Email
from .logout import logout_required

account_route = Blueprint('account_route', __name__)


def send_delete_request_email(user):
    token = url_serializer.dumps(user.email, salt='user-delete-request')
    link = url_for('account_route.cancel_account_delete',
                   token=token, _external=True)
    datetime = user.delete_request_formated + ' UTC'
    msg = render_template(
        'account_delete.html', name=user.name, datetime=datetime, interval=current_app.config['ACCOUNT_DELETE_INTERVAL'], link=link)

    email = Email(subject='Account Delete Request', body=msg, recipient=user)
    db.session.add(email)
    db.session.commit()
    email_sender.set()


def save_picture(picture):
    while True:
        name = secrets.token_hex(8)
        _, ext = os.path.splitext(picture.filename)
        filename = name + ext
        path = os.path.join(current_app.root_path,
                            'static/img/profile_pics', filename)

        if not os.path.exists(path):
            break

    img = Image.open(picture)
    img.thumbnail((250, 250))
    img.save(path)
    return filename


@account_route.route('/account', methods=['GET'])
@login_required
def account():
    try:
        form_data = session.pop('account-form-data')
        form_errors = session.pop('account-form-errors')
    except KeyError:
        form = UpdateAccountForm()
        form.name.data = current_user.name
        return render_template('account.html', title='Account', form=form)

    form = UpdateAccountForm(data=form_data)
    return render_template('account.html', title='Account', form=form, errors=form_errors)


@account_route.route('/account', methods=['POST'])
@login_required
def account_prg():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.name = form.name.data

        if form.picture.data:
            new_picture = save_picture(form.picture.data)
            current_user.delete_profile_picture()
            current_user.profile_pic = new_picture

        if form.new_password.data:
            current_user.password = form.new_password.data

        db.session.commit()
        flash('Changes saved.', 'success')
        return redirect(url_for('home_route.home'))

    form.picture.data = None
    session['account-form-data'] = form.data
    session['account-form-errors'] = form.errors
    return redirect(url_for('account_route.account'))


@account_route.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
    current_user.delete_request = datetime.utcnow()
    db.session.commit()
    send_delete_request_email(current_user)
    logout_user()
    flash('Account deletion requested successfully. A detailed email will be sent to you.', 'success')
    return redirect(url_for('home_route.home'))


@account_route.route('/account/delete/<token>')
@logout_required
def cancel_account_delete(token):
    try:
        email = url_serializer.loads(token, salt='user-delete-request')
        user = User.query.filter_by(email=email).first()

        if user:
            user.delete_request = None
            db.session.commit()
            flash('Deletion request canceled.', 'success')
        else:
            flash('Account not found.', 'danger')
    except:
        flash('Invalid link.', 'danger')

    return redirect(url_for('login_route.login'))
