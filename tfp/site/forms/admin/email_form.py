from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, BooleanField, DateTimeField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class NewEmailForm(FlaskForm):
    recipient = SelectField(
        'Recipient', validators=[DataRequired()])
    subject = StringField('Subject', validators=[
                          DataRequired(), Length(max=100)])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditEmailForm(FlaskForm):
    recipient = SelectField(
        'Recipient', validators=[DataRequired()])
    subject = StringField('Subject', validators=[
                          DataRequired(), Length(max=100)])
    body = TextAreaField('Body', validators=[DataRequired()])
    sent = BooleanField('Sent')
    sending_attempts = IntegerField('Sending Attempts', validators=[
                                    NumberRange(min=0, max=10)])
    next_sending_try = DateTimeField(
        'Next Sending Try', format='%m/%d/%Y %H:%M', validators=[DataRequired()])
    submit = SubmitField('Save')
