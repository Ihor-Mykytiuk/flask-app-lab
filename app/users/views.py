from datetime import datetime, timedelta

from flask import render_template, request, redirect, url_for, make_response, session, flash
from . import users_bp


@users_bp.route('/profile', methods=['GET', 'POST'])
def get_profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть, щоб переглянути профіль.', 'danger')
        return redirect(url_for('users.login'))
    username = session['username']
    cookies = request.cookies
    if request.method == 'POST':
        if 'add_cookie' in request.form:
            # Додати кукі
            cookie_key = request.form.get('cookie_key')
            cookie_value = request.form.get('cookie_value')
            cookie_expire = int(request.form.get('cookie_expire', 0))
            resp = make_response(redirect(url_for('users.get_profile')))
            resp.set_cookie(cookie_key, cookie_value, max_age=cookie_expire)
            flash('Кукі успішно додано', 'success')
            return resp
        elif 'remove_cookie_by_key' in request.form:
            # Видалити кукі за ключем
            cookie_key = request.form.get('remove_key')
            resp = make_response(redirect(url_for('users.get_profile')))
            if cookie_key and cookie_key in cookies:
                resp.set_cookie(cookie_key, '', expires=0)
                flash('Кукі успішно видалено', 'success')
            else:
                flash('Кукі з таким ключем не знайдено', 'danger')
            return resp
        elif 'remove_all_cookies' in request.form:
            # Видалити всі кукі
            resp = make_response(redirect(url_for('users.get_profile')))
            for key in cookies:
                resp.set_cookie(key, '', expires=0)
            flash('Всі кукі успішно видалено', 'success')
            return resp
    return render_template('profile.html', username=username, cookies=cookies)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if username == "Ihor" and password == "123":
            flash("Вхід виконано успішно", "success")
            session["username"] = username
            return redirect(url_for("users.get_profile"))
        else:
            flash("Неправильний логін або пароль", "danger")
    return render_template('login.html')


@users_bp.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("users.get_profile"))


@users_bp.route('/hi/<string:name>/')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, type=int)
    return render_template('hi.html', name=name, age=age)


@users_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", _external=True)
    return redirect(to_url)


@users_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=10))
    return response


@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'


@users_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0)  # response.set_cookie('username', '', max_age=0)
    return response
