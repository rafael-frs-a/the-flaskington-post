from flask import Blueprint, render_template, redirect, url_for, request
from tfp.ext.database import db
from tfp.site.models.post import get_posts, Post

admin_post_route = Blueprint('admin_post_route', __name__)


@admin_post_route.route('/admin/post')
def post():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    desc = request.args.get('desc')
    per_page = 10

    if sort:
        posts = get_posts(per_page, page, sort, desc)
    else:
        posts = get_posts(per_page, page, 'date_posted', True)

    return render_template('admin/post.html', title='Post', posts=posts)


@admin_post_route.route('/admin/post/<title_slug>', methods=['GET'])
def view_post(title_slug):
    post = Post.query.filter_by(title_slug=title_slug).first_or_404()
    return render_template('admin/post_form.html', title='Post', post=post,
                           url_back=url_for('admin_post_route.post'))


@admin_post_route.route('/admin/post/delete/<title_slug>', methods=['POST'])
def delete_post_prg(title_slug):
    post = Post.query.filter_by(title_slug=title_slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin_post_route.post'))
