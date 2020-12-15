import click
from datetime import datetime
from flask.cli import with_appcontext
from tfp.ext.database import db
from tfp.site.models.user import User, Role


@click.command(name='create_db')
@with_appcontext
def create_db():
    db.create_all()


@click.command(name='drop_db')
@with_appcontext
def drop_db():
    db.drop_all()


@click.command(name='create_admin')
@with_appcontext
def create_admin():
    role = Role.query.filter_by(name='admin').first()

    if not role:
        role = Role()
        role.name = 'admin'
        role.description = 'Admin role'
        db.session.add(role)
        db.session.commit()

    user = User.query.filter_by(username='admin').first()

    if not user:
        user = User()
        user.name = 'Admin'
        user.user_email = 'admin@tfp.com'
        user.password = 'admin'
        user.confirmed_at = datetime.utcnow()
        user.roles_names = ['admin']
        db.session.add(user)
        db.session.commit()


def init_app(app):
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(create_admin)
