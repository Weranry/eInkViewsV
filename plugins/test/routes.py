from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes

PLUGIN_NAME = "test"
PLUGIN_DESCRIPTION = "测试插件，生成从 m 到 h4xl 的测试图"

bp = Blueprint(PLUGIN_NAME, __name__)
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "view"))