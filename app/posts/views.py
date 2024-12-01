import os, json
from . import posts_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm
from .models import Post
from .. import db

POST_FILE = 'app/posts/posts.json'


def load_json_data(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def save_json_data(file, data):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)

# posts = load_json_data(POST_FILE)

@posts_bp.route('/')
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('posts.html', posts=posts)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        published_date = form.publish_date.data
        category = form.category.data
        author = session.get('username', None)
        new_post = Post(title=title,
                        content=content,
                        is_active=is_active,
                        posted=published_date,
                        category=category,
                        author=author)
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post '{title}' has been added.", 'success')
        return redirect(url_for('.get_posts'))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")

    return render_template('add_post.html', form=form)

@posts_bp.route('/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail_post.html', post=post)

@posts_bp.route('/remove_post/<int:post_id>')
def remove_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been removed.", 'success')
    return redirect(url_for('.get_posts'))

@posts_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        db.session.commit()
        flash(f"Post '{post.title}' has been updated.", 'success')
        return redirect(url_for('.get_posts'))
    return render_template('edit_post.html', form=form)