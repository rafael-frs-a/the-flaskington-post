from flask import Blueprint, session, render_template, redirect, url_for, flash
from tfp.ext.database import db
from tfp.ext.url_serializer import url_serializer
from tfp.services.email_sender import email_sender
from tfp.site.forms.register_form import RegisterForm
from tfp.site.models.user import User
from tfp.site.models.email import Email
from .logout import logout_required

register_route = Blueprint('register_route', __name__)


def send_confirmation_email(user):
    token = url_serializer.dumps(user.email, salt='email-confirm')
    link = url_for('account_confirm_route.confirm_account',
                   token=token, _external=True)
    msg = render_template(
        'account_confirm.html', name=user.name, link=link)

    email = Email(subject='Account Confirm', body=msg, recipient=user)
    db.session.add(email)
    db.session.commit()
    email_sender.set()


@register_route.route('/register', methods=['GET'])
@logout_required
def register():
    try:
        form_data = session.pop('register-form-data')
        form_errors = session.pop('register-form-errors')
    except KeyError:
        return render_template('register.html', title='Sign Up', form=RegisterForm())

    return render_template('register.html', title='Sign Up', form=RegisterForm(data=form_data), errors=form_errors)


@register_route.route('/register', methods=['POST'])
@logout_required
def register_prg():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(name=form.name.data, user_email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(user)
        flash(
            'A verification email will be sent to you. Please confirm your account before login.', 'success')
        return redirect(url_for('login_route.login'))

    session['register-form-data'] = form.data
    session['register-form-errors'] = form.errors
    return redirect(url_for('register_route.register'))
