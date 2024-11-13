import os, json
from . import posts_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm

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

posts = load_json_data(POST_FILE)

@posts_bp.route('/')
def get_posts():
    return render_template('posts.html', posts=posts)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "published_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "category": form.category.data,
            "author": session.get('username', 'Anonymous')
        }
        posts.append(new_post)
        save_json_data(POST_FILE, posts)
        flash(f"Post '{new_post['title']}' has been added.", 'success')
        return redirect(url_for('.get_posts'))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")

    return render_template('add_post.html', form=form)

@posts_bp.route('/<int:post_id>')
def get_post(post_id):
    if post_id < 1 or post_id > len(posts):
        abort(404)
    post = posts[post_id - 1]
    return render_template('detail_post.html', post=post)