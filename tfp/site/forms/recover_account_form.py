from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from .validators import password_length_validation


class RecoverAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Recovery Email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
                             DataRequired(), password_length_validation])
    submit = SubmitField('Save')
