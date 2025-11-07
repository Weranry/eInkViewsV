from flask import Blueprint, send_from_directory
import os

bp_templates = Blueprint('templates', __name__)

# 获取 public/pages 目录的绝对路径
PUBLIC_PAGES_DIR = os.path.join(os.path.dirname(__file__), '../../public/pages')
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '../../public')
@bp_templates.route('/')
def index():
    return send_from_directory(PUBLIC_PAGES_DIR, 'index.html')
@bp_templates.route('/favicon.ico')
def favicon():
    return send_from_directory(PUBLIC_DIR, 'favicon.ico')