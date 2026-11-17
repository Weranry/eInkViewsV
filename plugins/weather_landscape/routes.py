from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes
#from modules.register.auto_json_routes import register_json_routes
#from modules.register.auto_page_routes import register_page_routes

bp = Blueprint('weather_landscape', __name__)
PLUGIN_NAME = 'weather_landscape'
PLUGIN_DESCRIPTION = 'Weather landscape view plugin (ported)'

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'view')
#JSON_MODULE_DIR = os.path.join(os.path.dirname(__file__), 'json_module')
#PAGE_DIR = os.path.join(os.path.dirname(__file__), 'pages')

register_view_routes(bp, PLUGIN_NAME, VIEW_DIR)
#register_json_routes(bp, PLUGIN_NAME, JSON_MODULE_DIR)
#register_page_routes(bp, PLUGIN_NAME, PAGE_DIR)