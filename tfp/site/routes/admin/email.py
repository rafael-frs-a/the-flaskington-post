from flask import Blueprint, render_template, redirect, url_for, request, session
from tfp.services.email_sender import email_sender
from tfp.ext.database import db
from tfp.site.models.email import get_emails, Email
from tfp.site.models.user import User
from tfp.site.forms.admin.email_form import NewEmailForm, EditEmailForm
from ..utils import get_cleaned_html

admin_email_route = Blueprint('admin_email_route', __name__)


def feed_recipient_choices(form):
    users = User.query.order_by(User.email).all()
    form.recipient.choices = [(_.username, _.email) for _ in users]


def route_email_form(email):
    if email:
        cls_form = EditEmailForm
        template = 'admin/email_form_edit.html'
    else:
        cls_form = NewEmailForm
        template = 'admin/email_form_new.html'

    try:
        form_data = session.pop('email-form-data')
        form_errors = session.pop('email-form-errors')
    except:
        form = cls_form()
        feed_recipient_choices(form)

        if cls_form is EditEmailForm:
            form.recipient.data = email.recipient_username
            form.subject.data = email.subject
            form.body.data = email.body
            form.sent.data = email.sent
            form.sending_attempts.data = email.send_tries
            form.next_sending_try.data = email.next_try

        return render_template(template, title='Email',
                               form=form, url_back=url_for('admin_email_route.email'))

    form = cls_form(data=form_data)
    feed_recipient_choices(form)
    return render_template(template, title='Email', form=form,
                           errors=form_errors, url_back=url_for('admin_email_route.email'))


@admin_email_route.route('/admin/email')
def email():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    desc = request.args.get('desc')
    per_page = 10

    if sort:
        emails = get_emails(per_page, page, sort, desc)
    else:
        emails = get_emails(per_page, page, 'created_at', True)

    return render_template('admin/email.html', title='Email', emails=emails)


@admin_email_route.route('/admin/email/delete/<email_ids>', methods=['POST'])
def delete_email(email_ids):
    email_ids = email_ids.split(',')

    for email_id in email_ids:
        try:
            id = int(email_id)
            email = Email.query.filter_by(id=id).first()

            if email:
                db.session.delete(email)
        except:
            pass

    db.session.commit()
    return redirect(request.referrer if request.referrer else url_for('admin_email_route.email'))


@admin_email_route.route('/admin/email/new', methods=['GET'])
def new_email():
    return route_email_form(None)


@admin_email_route.route('/admin/email/new', methods=['POST'])
def new_email_prg():
    form = NewEmailForm()
    feed_recipient_choices(form)

    if form.validate_on_submit():
        email = Email(recipient_username=form.recipient.data,
                      subject=form.subject.data, body=form.body.data)
        db.session.add(email)
        db.session.commit()
        email_sender.set()
        return redirect(url_for('admin_email_route.email'))

    session['email-form-data'] = form.data
    session['email-form-errors'] = form.errors
    return redirect(url_for('admin_email_route.new_email'))


@admin_email_route.route('/admin/email/<int:id>', methods=['GET'])
def edit_email(id):
    email = Email.query.filter_by(id=id).first_or_404()
    return route_email_form(email)


@admin_email_route.route('/admin/email/<int:id>', methods=['POST'])
def edit_email_prg(id):
    email = Email.query.filter_by(id=id).first_or_404()
    form = EditEmailForm()
    feed_recipient_choices(form)

    if form.validate_on_submit():
        email.recipient_username = form.recipient.data
        email.subject = form.subject.data
        email.body = get_cleaned_html(form.body.data)
        email.sent = form.sent.data
        email.send_tries = form.sending_attempts.data
        email.next_try = form.next_sending_try.data
        db.session.commit()
        email_sender.set()
        return redirect(url_for('admin_email_route.email'))

    session['email-form-data'] = form.data
    session['email-form-errors'] = form.errors
    return redirect(url_for('admin_email_route.edit_email', id=id))
