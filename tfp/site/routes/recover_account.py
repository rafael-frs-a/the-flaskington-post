from flask import Blueprint, session, render_template, redirect, url_for, flash
from flask_mail import Message
from tfp.ext.mail import mail
from tfp.ext.url_serializer import url_timed_serializer
from tfp.ext.database import db
from tfp.site.models.user import User
from tfp.site.forms.recover_account_form import RecoverAccountForm, ResetPasswordForm
from .logout import logout_required

recover_account_route = Blueprint('recover_account_route', __name__)

EXPIRATION_TIME = 15  # 15 minutes


def send_recovery_email(user):
    token = url_timed_serializer.dumps(user.email, salt='recover-account')
    msg = Message('Account Recovery', recipients=[user.email])
    link = url_for('recover_account_route.recover_account_pwd',
                   token=token, _external=True)
    msg.html = render_template(
        'recover_account_mail.html', name=user.name, link=link, time=EXPIRATION_TIME)
    mail.send(msg)
    flash('A recovery email was sent to you.', 'success')


def get_user_from_email(email):
    return User.query.filter_by(email=email).filter_by(banned=False).first()


def get_user_from_token(token):
    user = None

    try:
        email = url_timed_serializer.loads(
            token, salt='recover-account', max_age=EXPIRATION_TIME * 60)
        user = get_user_from_email(email)

        if not user:
            flash('Invalid recovery link.', 'danger')
    except:
        flash('Invalid recovery link.', 'danger')

    return user


@recover_account_route.route('/recover-account/<token>', methods=['GET'])
@logout_required
def recover_account_pwd(token):
    user = get_user_from_token(token)

    if not user:
        return redirect(url_for('login_route.login'))

    try:
        form_data = session.pop('reset-form-data')
        form_errors = session.pop('reset-form-errors')
    except KeyError:
        return render_template('reset_password.html', title='Reset Password', form=ResetPasswordForm())

    return render_template('reset_password.html', title='Reset Password', form=ResetPasswordForm(data=form_data), errors=form_errors)


@recover_account_route.route('/recover-account/<token>', methods=['POST'])
@logout_required
def recover_account_pwd_prg(token):
    user = get_user_from_token(token)

    if not user:
        return redirect(url_for('login_route.login'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Password reset.', 'success')
        return redirect(url_for('login_route.login'))

    session['reset-form-data'] = form.data
    session['reset-form-errors'] = form.errors
    return redirect(url_for('recover_account_route.recover_account_pwd', token=token))


@recover_account_route.route('/recover-account', methods=['GET'])
@logout_required
def recover_account():
    try:
        form_data = session.pop('recover-form-data')
        form_errors = session.pop('recover-form-errors')
    except KeyError:
        return render_template('recover_account.html', title='Recover Account', form=RecoverAccountForm())

    return render_template('recover_account.html', title='Recover Account', form=RecoverAccountForm(data=form_data), errors=form_errors)


@recover_account_route.route('/recover-account', methods=['POST'])
@logout_required
def recover_account_prg():
    form = RecoverAccountForm()

    if form.validate_on_submit():
        user = get_user_from_email(form.email.data)

        if user:
            try:
                send_recovery_email(user)
                return redirect(url_for('login_route.login'))
            except:
                flash('Something went wrong. Please try again later.', 'danger')
        else:
            flash('Account not found. Please verify the email informed.', 'danger')

    session['recover-form-data'] = form.data
    session['recover-form-errors'] = form.errors
    return redirect(url_for('recover_account_route.recover_account'))
