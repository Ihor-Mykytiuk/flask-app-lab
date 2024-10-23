from flask import render_template, request, redirect, url_for
from . import users_bp


@users_bp.route('/hi/<string:name>/')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, type=int)
    return render_template('hi.html', name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", _external=True)
    return redirect(to_url)
