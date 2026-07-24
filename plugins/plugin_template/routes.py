from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes
from modules.register.auto_json_routes import register_json_routes
from modules.register.auto_page_routes import register_page_routes

PLUGIN_NAME = "your_plugin"
PLUGIN_DESCRIPTION = "插件模板"

bp = Blueprint(PLUGIN_NAME, __name__)
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "view"))
register_json_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "json_module"))
register_page_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "page"))
