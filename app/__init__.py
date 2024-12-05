from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='config'):
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
        from . import views
        from app.users import users_bp
        from app.posts import posts_bp

        app.register_blueprint(posts_bp)
        app.register_blueprint(users_bp)

    return app
