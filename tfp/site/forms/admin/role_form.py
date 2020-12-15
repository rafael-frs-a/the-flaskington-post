from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from tfp.site.models.user import Role


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=40)])
    description = TextAreaField('Description', validators=[Length(max=100)])
    submit = SubmitField('Save')
    current_role = None

    def validate_name(self, name):
        if name.data and (not self.current_role or self.current_role.name != name.data):
            role = Role.query.filter_by(name=name.data).first()

            if role:
                raise ValidationError('Role name already taken.')
