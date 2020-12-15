from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, SelectMultipleField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, ValidationError
from tfp.site.models.user import User
from ..validators import password_length_validation
from ..custom_fields import NullableDateTimeField


class AdminNewUserForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), password_length_validation])
    roles = SelectMultipleField('Roles')
    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already taken.')


class AdminEditUserForm(FlaskForm):
    roles = SelectMultipleField('Roles')
    delete_request = NullableDateTimeField(
        'Delete Request', format='%m/%d/%Y %H:%M')
    banned = BooleanField('Banned')
    ban_reason = TextAreaField(
        'Reason of Banishment', validators=[Length(max=200)])
    submit = SubmitField('Save')
    current_user = None

    def validate_ban_reason(self, ban_reason):
        if self.banned.data and not ban_reason.data and (not self.current_user or not self.current_user.banned):
            raise ValidationError('This field is required.')
