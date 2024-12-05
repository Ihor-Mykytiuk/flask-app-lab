from flask import Blueprint


main_bp = Blueprint('main', __name__, url_prefix='/', template_folder='templates/main')

from . import views