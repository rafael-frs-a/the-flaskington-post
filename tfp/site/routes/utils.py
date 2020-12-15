import bleach
from flask import current_app


def get_cleaned_html(html):
    return bleach.clean(html, tags=current_app.config['ALLOWED_POST_TAGS'],
                        attributes=current_app.config['ALLOWED_POST_ATTRIBUTES'],
                        styles=current_app.config['ALLOWED_POST_STYLES'])


def get_form_errors(form):
    errors = {}

    for field in form:
        if field.errors:
            errors[field.name + '_error'] = ' '.join(field.errors)

    return errors
