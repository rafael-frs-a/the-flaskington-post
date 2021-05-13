from datetime import datetime, timedelta
from flask import abort
from sqlalchemy import event, or_, asc, desc
from sqlalchemy.sql import select
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import slugify
from tfp.ext.database import db
from .user import User


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    title_slug = db.Column(db.Unicode, nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)

    timezone = 0

    def _get_date_formated(self, dt):
        if not dt:
            return ''

        return (dt - timedelta(minutes=self.timezone)).strftime('%d %b %Y, %H:%M')

    @property
    def date_posted_formated(self):
        return self._get_date_formated(self.date_posted)

    @property
    def date_edited_formated(self):
        return self._get_date_formated(self.date_edited)

    @property
    def post_title(self):
        return self.title

    @post_title.setter
    def post_title(self, title):
        self.title = title
        self.title_slug = get_title_slug(title)

    @hybrid_property
    def author_name(self):
        return self.author.name

    @author_name.expression
    def author_name(cls):
        return select([User.name]).where(User.id == cls.user_id)

    def __repr__(self):
        return f'Post({self.title}, {self.title_slug}, {self.author.name}, {self.date_posted}, {self.date_edited})'


@event.listens_for(Post, 'before_update')
def receive_before_update(mapper, connection, target):
    target.date_edited = datetime.utcnow()


def get_posts(per_page, page, order_field, desc_):
    direction = desc if desc_ else asc

    try:
        return Post.query.order_by(direction(getattr(Post, order_field))).paginate(
            per_page=per_page, page=page)
    except:
        abort(404)


def get_title_slug(title):
    return slugify(title)


def get_post(title_slug):
    return Post.query.filter_by(title_slug=title_slug).first_or_404()


def get_all_posts_filter(page, filter):
    return Post.query.join(Post.author, aliased=True).filter(
        User.banned == False).filter(or_(
            Post.title.ilike(f'%{filter}%'), Post.content.ilike(f'%{filter}%'),
            Post.author.has(User.name.ilike(f'%{filter}%')))).order_by(
        Post.date_posted.desc(), Post.id.desc()).paginate(page=page, per_page=5)


def get_posts_by_author_filter(page, author, filter):
    return Post.query.filter_by(author=author).join(Post.author, aliased=True).filter(
        User.banned == False).filter(or_(
            Post.title.ilike(f'%{filter}%'), Post.content.ilike(f'%{filter}%'),
            Post.author.has(User.name.ilike(f'%{filter}%')))).order_by(
        Post.date_posted.desc(), Post.id.desc()).paginate(page=page, per_page=5)
