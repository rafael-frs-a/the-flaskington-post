from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from tfp.site.models.post import Post, get_title_slug


class PostForm(FlaskForm):
    title = StringField('TItle', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    current_post = None

    def validate_title(self, title):
        if title.data:
            title_slug = get_title_slug(title.data)

            if not title_slug:
                raise ValidationError('Invalid title.')

            if self.current_post and title_slug == self.current_post.title_slug:
                return

            if Post.query.filter_by(title_slug=title_slug).first():
                raise ValidationError(
                    'A similar post title already exists. Please, choose a different one.')

    def validate_content(self, content):
        if content.data and len(content.data.encode('utf-8')) > 2E4:
            raise ValidationError('Content too large.')
