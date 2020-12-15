from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from tfp.site.models.user import User
from .validators import password_length_validation


class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=40)])
    picture = FileField('Profile Picture')
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[
                                 password_length_validation])
    submit = SubmitField('Save')

    def validate_current_password(self, password):
        if password.data and not current_user.password_match(password.data):
            raise ValidationError('Incorrect password.')

    def validate_new_password(self, password):
        if self.current_password.data and not password.data:
            raise ValidationError('New password not informed.')

    def validate_picture(self, picture):
        if picture.data:
            extension = picture.data.filename.split('.')[-1]

            if extension.lower() not in current_app.config['ALLOWED_PROFILE_PICS']:
                extensions = ', '.join(
                    current_app.config['ALLOWED_PROFILE_PICS'])
                raise ValidationError(
                    f'File does not have an approved extension: {extensions}')
