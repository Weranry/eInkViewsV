from fastapi import APIRouter
import os
from modules.register.auto_view_routes import register_view_routes

PLUGIN_NAME = "astro"
PLUGIN_DESCRIPTION = "天文插件，提供月相视图，通过经纬度返回月相图案和信息"

router = APIRouter()
plugin_dir = os.path.dirname(os.path.abspath(__file__))

register_view_routes(router, PLUGIN_NAME, os.path.join(plugin_dir, "view"))
