import os
from time import time
from datetime import datetime
from threading import Thread, Event
from tfp.ext.database import db
from tfp.site.models.user import get_users_delete

user_deleter = Event()


def init_user_deleter(app):
    def delete_users(app, user_deleter, interval):
        while True:
            start = time()
            print(f'{datetime.now()}: Checking for users with delete request...')

            with app.app_context():
                users = get_users_delete(app.config['ACCOUNT_DELETE_INTERVAL'])

                if len(users) > 0:
                    print('Starting to delete users...')

                    for user in users:
                        db.session.delete(user)

                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()

                    print(len(users), 'users deleted...')
                else:
                    print('No users found for deleting...')

            duration = time() - start

            if duration < interval:
                user_deleter.clear()
                user_deleter.wait(interval - duration)

    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        Thread(name='User deleter', target=delete_users, args=[
               app, user_deleter, app.config['DELETE_USERS_INTERVAL']], daemon=True).start()
