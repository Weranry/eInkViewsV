from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes

PLUGIN_NAME = "cal"
PLUGIN_DESCRIPTION = "日历插件，支持公历、农历、干支、节气、宜忌"

bp = Blueprint(PLUGIN_NAME, __name__)
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "view"))