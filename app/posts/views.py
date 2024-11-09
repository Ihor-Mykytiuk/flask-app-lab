from . import posts_bp
from flask import render_template, abort, flash, redirect, url_for
from .forms import PostForm

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@posts_bp.route('/')
def get_posts():
    return render_template('posts.html', posts=posts)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        flash(f"Post '{title}' has been added.", 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add_post.html', form=form)

@posts_bp.route('/<int:id>')
def get_post(id):
    if id < 1 or id > len(posts):
        abort(404)
    post = posts[id-1]
    return render_template('detail_post.html', post=post)