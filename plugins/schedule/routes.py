import os
from flask import Blueprint
from modules.register.auto_view_routes import register_view_routes
from modules.register.auto_page_routes import register_page_routes

bp = Blueprint('schedule', __name__)
PLUGIN_NAME = 'schedule'
PLUGIN_DESCRIPTION = '课程表插件'

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'view')
PAGE_DIR = os.path.join(os.path.dirname(__file__), 'page')

register_view_routes(bp, PLUGIN_NAME, VIEW_DIR)
register_page_routes(bp, PLUGIN_NAME, PAGE_DIR)
