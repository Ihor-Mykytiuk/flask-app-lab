from flask import render_template, abort, flash, redirect, url_for, session, request
from . import main_bp

@main_bp.route('/')
def main():
    return render_template('hello.html')

@main_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template('home.html', agent=agent)

@main_bp.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')
