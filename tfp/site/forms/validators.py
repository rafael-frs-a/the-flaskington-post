from wtforms.validators import ValidationError


def password_length_validation(form, field):
    if field.data and len(field.data) < 8:
        raise ValidationError('Field must be at least 8 characters long.')
