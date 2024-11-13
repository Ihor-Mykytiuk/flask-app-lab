from flask import Blueprint

posts_bp = Blueprint('post', __name__, url_prefix='/post', template_folder='templates/posts',
static_folder = "static",
static_url_path = "static_for_posts"
)

from . import views
