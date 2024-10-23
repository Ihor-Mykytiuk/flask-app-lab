from flask import Blueprint

posts_bp = Blueprint('post', __name__, url_prefix='/post', template_folder='templates/posts')

from . import views
