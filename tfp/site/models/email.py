from datetime import datetime
from sqlalchemy import asc, desc, and_
from sqlalchemy.sql import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from tfp.ext.database import db
from .user import User


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Unicode, nullable=False)
    body = db.Column(db.Unicode, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    send_tries = db.Column(db.Integer, nullable=False, default=0)
    next_try = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sent = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)

    recipient_username = association_proxy(
        'recipient', 'username', creator=lambda username: User.query.filter_by(username=username).first_or_404())

    def _get_date_formated(self, dt):
        if not dt:
            return ''

        return dt.strftime('%d %b %Y, %H:%M')

    @property
    def created_at_formated(self):
        return self._get_date_formated(self.created_at)

    @property
    def next_try_formated(self):
        return self._get_date_formated(self.next_try)

    @hybrid_property
    def recipient_name(self):
        return self.recipient.name

    @recipient_name.expression
    def recipient_name(cls):
        from .user import User
        return select([User.name]).where(User.id == cls.user_id)

    def __repr__(self):
        return f'Email({self.subject}, {self.created_at}, {self.recipient.email}, {self.send_tries}, {self.next_try}, {self.sent})'


def get_emails_for_sending():
    now = datetime.utcnow()
    return Email.query.filter_by(sent=False).filter(and_(
        Email.send_tries < 10, Email.next_try <= now)).order_by(Email.created_at).all()


def get_emails(per_page, page, order_field, desc_):
    direction = desc if desc_ else asc
    return Email.query.order_by(direction(getattr(Email, order_field))).paginate(
        per_page=per_page, page=page)
