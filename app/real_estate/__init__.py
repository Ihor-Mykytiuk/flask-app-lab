from flask import Blueprint

real_estate_bp = Blueprint('real_estate', __name__,
                           url_prefix='/real-estate',
                           template_folder='templates/real_estate',
                           static_folder = "static",
)

from . import views
