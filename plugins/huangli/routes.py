from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes

PLUGIN_NAME = "huangli"
PLUGIN_DESCRIPTION = "黄历插件，展示当日完整的黄历信息，包含宜忌、吉神凶煞、冲煞、彭祖百忌等"

bp = Blueprint(PLUGIN_NAME, __name__)
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(bp, PLUGIN_NAME, os.path.join(plugin_dir, "view"))