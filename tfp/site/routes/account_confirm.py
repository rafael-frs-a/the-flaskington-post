from datetime import datetime
from flask import Blueprint, redirect, url_for, flash
from tfp.ext.database import db
from tfp.ext.url_serializer import url_serializer
from tfp.site.models.user import User
from .logout import logout_required

account_confirm_route = Blueprint('account_confirm_route', __name__)


@account_confirm_route.route('/confirm-account/<token>')
@logout_required
def confirm_account(token):
    try:
        email = url_serializer.loads(token, salt='email-confirm')
        user = User.query.filter_by(email=email).first()

        if user:
            user.confirmed_at = datetime.utcnow()
            db.session.commit()
            flash('Account confirmed.', 'success')
        else:
            flash('Invalid confirmation link.', 'danger')
    except:
        flash('Invalid confirmation link.', 'danger')

    return redirect(url_for('login_route.login'))
