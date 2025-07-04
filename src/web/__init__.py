from flask import Blueprint

web_bp = Blueprint('web', __name__)

from . import app  # Import the app module to register routes and views