from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, current_user
from datetime import datetime as dt

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Будь ласка, увійдіть, щоб переглянути цю сторінку.'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from app.main import main_bp
        from app.users import users_bp
        from app.posts import posts_bp
        from app.real_estate import real_estate_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(posts_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(real_estate_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = dt.now()
            db.session.commit()

    return app
