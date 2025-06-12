from flask import Blueprint

statistics_bp = Blueprint('statistics', __name__)

from . import routes
