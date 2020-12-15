from datetime import datetime
from tfp.ext.database import db
from tfp.site.models.user import User, Role


def init_app(app):
    @app.cli.command()
    def create_db():
        db.create_all()

    @app.cli.command()
    def drop_db():
        db.drop_all()

    @app.cli.command()
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
