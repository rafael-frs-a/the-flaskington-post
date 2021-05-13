import os
from time import time
from datetime import timedelta, datetime
from threading import Thread, Event
from flask_mail import Message
from tfp.ext.mail import mail
from tfp.ext.database import db
from tfp.site.models.email import get_emails_for_sending

email_sender = Event()


def init_email_sender(app):
    def send_emails(app, email_sender, interval):
        while True:
            start = time()
            print(f'{datetime.now()}: Checking for emails to send...')

            with app.app_context():
                emails = get_emails_for_sending()

                if len(emails) > 0:
                    try:
                        with mail.connect() as conn:
                            for email in emails:
                                msg = Message(subject=email.subject, recipients=[
                                              email.recipient.email])
                                msg.html = email.body

                                try:
                                    conn.send(msg)
                                    email.sent = True
                                except:
                                    email.next_try = datetime.utcnow() + timedelta(seconds=interval *
                                                                                   2 ** email.send_tries)
                                finally:
                                    try:
                                        email.send_tries += 1
                                        db.session.commit()
                                    except:
                                        db.session.rollback()

                        print(len(emails), 'emails sent...')
                    except:
                        pass

            duration = time() - start

            if duration < interval:
                email_sender.clear()
                email_sender.wait(interval - duration)

    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        Thread(name='Email sender', target=send_emails, args=[
               app, email_sender, app.config['MAIL_SEND_INTERVAL']], daemon=True).start()
