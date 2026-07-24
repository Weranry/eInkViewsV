from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes

PLUGIN_NAME = "dashboard"
PLUGIN_DESCRIPTION = "综合信息仪表盘，包含日历、天气、一言、新闻"

bp = Blueprint(PLUGIN_NAME, __name__)
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "view"))