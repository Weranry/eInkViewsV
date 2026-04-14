from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes

bp = Blueprint('openmeteo', __name__)
PLUGIN_NAME = 'openmeteo'
PLUGIN_DESCRIPTION = 'OpenMeteo Air Quality Plugin'

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'view')

register_view_routes(bp, PLUGIN_NAME, VIEW_DIR)
