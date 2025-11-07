import os
from PIL import ImageFont

# 获取项目根目录下的字体路径
def get_root_font_path(filename):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    return os.path.join(project_root, 'assets', 'font', filename)

# 获取插件目录下的字体路径
def get_plugin_font_path(filename, base_file=__file__):
    plugin_root = os.path.abspath(os.path.join(os.path.dirname(base_file), '../../..'))
    return os.path.join(plugin_root, 'assets', 'font', filename)

def _load_font(size, font_path):
    abs_path = os.path.abspath(font_path)
    try:
        return ImageFont.truetype(abs_path, size)
    except Exception as e:
        raise RuntimeError(f"字体加载失败: {abs_path} ({e})")

# 在视图模块中设定字体，大小
def get_font(size, font_path):
    return _load_font(size, font_path)
