from flask import Blueprint, render_template, redirect, url_for, current_app, abort, request, make_response
from flask_login import current_user, login_required
from tfp.ext.database import db
from tfp.site.forms.post_form import PostForm
from tfp.site.models.post import Post, get_post, get_all_posts_filter, get_posts_by_author_filter
from tfp.site.models.user import User
from .utils import get_cleaned_html, get_form_errors

posts_route = Blueprint('posts_route', __name__)


def get_post_data(post, add_link):
    post_data = {}

    if add_link:
        route = 'posts_route.view_post'
        post_data['title'] = f'<a class="text-black link-underline" href="{url_for(route, title_slug=post.title_slug)}">{post.title}</a>'
    else:
        post_data['title'] = post.title

    post_data['content'] = post.content
    route = 'posts_route.post_by_author'
    post_data['author'] = f'<a href="{url_for(route, username=post.author.username)}">{post.author.name}</a>'
    post_data['date_posted'] = f'Posted at {post.date_posted_formated}'

    if post.date_edited:
        post_data['date_edited'] = f'Last edited at {post.date_edited_formated}'

    post_data['edit_url'] = url_for(
        'posts_route.edit_post', title_slug=post.title_slug)
    post_data['author_img'] = f'''
        <a href="{url_for(route, username=post.author.username)}">
        <img class="rounded-circle author-img" src="{post.author.profile_pic_path}" alt="Picture Not Found" height="50px" width="50px">
        </a>
        '''

    post_data['is_author'] = current_user == post.author
    post_data['title_slug'] = post.title_slug

    return post_data


def get_posts_response(posts):
    posts_data = {}
    posts_data['posts'] = []

    for post in posts.items:
        posts_data['posts'].append(get_post_data(post, True))

    posts_data['has_next'] = posts.has_next
    return posts_data


def there_is_content(content):
    if not content:
        return False

    content = content.replace(' ', '')

    for tag in current_app.config['ALLOWED_POST_TAGS']:
        if not content:
            return False

        content = content.replace(f'<{tag}>', '')
        content = content.replace(f'</{tag}>', '')

    return content


def check_post_author(post):
    if post.author != current_user:
        abort(403)


def request_with_args():
    if 'page' in request.args:
        if 'timezone' in request.args:
            Post.timezone = request.args.get('timezone', type=int)

        return True

    return False


def home_posts():
    if request_with_args():
        page = request.args.get('page', type=int)
        filter = request.args.get('filter', '')
        posts = get_all_posts_filter(page, filter)
        posts_data = get_posts_response(posts)
        return make_response(posts_data, 200)

    return render_template('home.html', search=True, home=True)


@posts_route.route('/post/<title_slug>')
def view_post(title_slug):
    post = get_post(title_slug)

    if request_with_args():
        posts_data = {}
        posts_data['posts'] = []
        posts_data['posts'].append(get_post_data(post, False))
        posts_data['stop'] = True
        return make_response(posts_data, 200)

    return render_template('home.html', title=post.title)


@posts_route.route('/post/edit/<title_slug>', methods=['GET'])
@login_required
def edit_post(title_slug):
    post = get_post(title_slug)
    check_post_author(post)
    form = PostForm()
    form.title.data = post.title
    form.content.data = post.content
    form.current_post = post
    return render_template('compose.html', title='Edit Post', form=form)


@posts_route.route('/post/edit/<title_slug>', methods=['POST'])
@login_required
def edit_post_ajax(title_slug):
    post = get_post(title_slug)
    form = PostForm()
    form.current_post = post

    if not there_is_content(form.content.data):
        form.content.data = None

    if form.validate_on_submit():
        cleaned_html = get_cleaned_html(form.content.data)
        check_post_author(post)
        post.post_title = form.title.data
        post.content = cleaned_html
        db.session.commit()
        return {'success': 'success'}

    return get_form_errors(form)


@posts_route.route('/post/delete/<title_slug>', methods=['POST'])
@login_required
def delete_post(title_slug):
    post = get_post(title_slug)
    check_post_author(post)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home_route.home'))


@posts_route.route('/post/new', methods=['GET'])
@login_required
def new_post():
    form = PostForm()
    return render_template('compose.html', title='Compose', form=form)


@posts_route.route('/post/new', methods=['POST'])
@login_required
def new_post_ajax():
    form = PostForm()

    if not there_is_content(form.content.data):
        form.content.data = None

    if form.validate_on_submit():
        cleaned_html = get_cleaned_html(form.content.data)
        post = Post(post_title=form.title.data,
                    content=cleaned_html, author=current_user)
        db.session.add(post)
        db.session.commit()
        return {'success': 'success'}

    return get_form_errors(form)


@posts_route.route('/user/<username>')
def post_by_author(username):
    user = User.query.filter_by(username=username).first_or_404()

    if request_with_args():
        page = request.args.get('page', type=int)
        filter = request.args.get('filter', '')
        posts = get_posts_by_author_filter(page, user, filter)
        posts_data = get_posts_response(posts)
        return make_response(posts_data, 200)

    return render_template('home.html', search=True, home=True, author=user, total_posts=user.posts_count)
