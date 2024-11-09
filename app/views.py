from flask import Flask, request, redirect, url_for, render_template, abort
from . import app


@app.route('/')
def main():
    return render_template('hello.html')

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template('home.html', agent=agent)

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404