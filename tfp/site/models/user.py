import os
from datetime import datetime, timedelta
from random import randint
from flask import url_for, current_app, abort
from flask_login import UserMixin
from sqlalchemy import asc, desc, func, event, and_
from sqlalchemy.sql import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from slugify import slugify
from tfp.ext.database import db
from tfp.ext.login_manager import login_manager
from tfp.ext.hashing import bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(login_id=user_id).first()


role_user_table = db.Table('role_user',
                           db.Column('user_id', db.Integer(),
                                     db.ForeignKey('user.id', ondelete='CASCADE')),
                           db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


def get_rand_id():
    user_count = User.query.count()

    while True:
        rand_int = randint(1, 1E10 + user_count)

        if not User.query.filter_by(login_id=rand_int).first():
            return rand_int


class User(db.Model, UserMixin):
    DEFAULT_PROFILE_PIC = 'default.jpg'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.Unicode, nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    profile_pic = db.Column(
        db.String(20), nullable=False, default=DEFAULT_PROFILE_PIC)
    _password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    banned = db.Column(db.Boolean, nullable=False, default=False)
    login_id = db.Column(db.BigInteger, nullable=False,
                         unique=True, default=get_rand_id)
    delete_request = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='author',
                            lazy='dynamic', cascade='all, delete-orphan')
    emails = db.relationship('Email', backref='recipient',
                             lazy='select', cascade='all, delete-orphan')
    roles = db.relationship('Role', secondary=role_user_table,
                            backref='user', lazy='select')

    roles_names = association_proxy(
        'roles', 'name', creator=lambda name: Role.query.filter_by(name=name).first_or_404())

    def get_id(self):
        return str(self.login_id)

    def password_match(self, password):
        return bcrypt.check_password_hash(self._password, password)

    def has_role(self, role):
        role_row = Role.query.filter_by(name=role).first()

        if role_row:
            return role_row in self.roles

        return False

    def delete_profile_picture(self):
        if self.profile_pic == self.DEFAULT_PROFILE_PIC:
            return

        path = os.path.join(current_app.root_path,
                            'static/img/profile_pics', self.profile_pic)

        if os.path.exists(path):
            os.remove(path)

        self.profile_pic = self.DEFAULT_PROFILE_PIC

    def _get_date_formated(self, dt):
        if not dt:
            return ''

        return dt.strftime('%d %b %Y, %H:%M')

    @property
    def created_at_formated(self):
        return self._get_date_formated(self.created_at)

    @property
    def confirmed_at_formated(self):
        return self._get_date_formated(self.confirmed_at)

    @property
    def delete_request_formated(self):
        return self._get_date_formated(self.delete_request)

    @hybrid_property
    def roles_formated(self):
        roles = sorted([_.name for _ in self.roles])
        return ', '.join(roles)

    @roles_formated.expression
    def roles_formated(cls):
        return select([func.count(role_user_table.c.role_id)]).where(role_user_table.c.user_id == cls.id)

    @property
    def profile_pic_path(self):
        return url_for('static', filename='img/profile_pics/' + self.profile_pic)

    @hybrid_property
    def posts_count(self):
        return self.posts.count()

    @posts_count.expression
    def posts_count(cls):
        from .post import Post
        return select([func.count(Post.id)]).where(Post.user_id == cls.id)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(
            password).decode('utf-8')

    @property
    def user_email(self):
        return self.email

    @user_email.setter
    def user_email(self, email):
        self.email = email
        slug = slugify(email.split('@')[0], separator='_')
        username = slug
        count = 1

        while User.query.filter_by(username=username).first():
            username = slug + str(count)
            count += 1

        self.username = username

    def __repr__(self):
        return f'User({self.name}, {self.username}, {self.email}, {self.profile_pic}, {self.confirmed_at})'


@event.listens_for(User, 'before_delete')
def receive_before_delete(mapper, connection, target):
    target.delete_profile_picture()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f'Role({self.name}, {self.description})'


def get_users(per_page, page, order_field, desc_):
    direction = desc if desc_ else asc

    try:
        return User.query.order_by(direction(getattr(User, order_field))).paginate(
            per_page=per_page, page=page)
    except:
        abort(404)


def get_users_delete(hours_interval):
    dt = datetime.utcnow() - timedelta(hours=hours_interval)
    return User.query.filter(and_(
        User.delete_request.isnot(None), User.delete_request < dt)).order_by(User.delete_request).all()


def get_roles(per_page, page, order_field, desc_):
    direction = desc if desc_ else asc

    try:
        return Role.query.order_by(direction(getattr(Role, order_field))).paginate(
            per_page=per_page, page=page)
    except:
        abort(404)
