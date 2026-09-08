import importlib
import os
from flask import Flask
import sys

def register_plugins(app: Flask, plugins_dir='plugins'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    abs_plugins_dir = os.path.join(project_root, plugins_dir)
    result = {'total': 0, 'success': 0, 'failed': 0, 'plugins': []}
    try:
        entries = os.listdir(abs_plugins_dir)
    except FileNotFoundError:
        print(f"插件目录不存在: {abs_plugins_dir}")
        return result
    plugin_names = [
        name for name in entries
        if os.path.isdir(os.path.join(abs_plugins_dir, name)) and os.path.exists(os.path.join(abs_plugins_dir, name, 'routes.py'))
    ]
    result['total'] = len(plugin_names)
    if not plugin_names:
        return result
    for plugin_name in plugin_names:
        routes_module = f'{plugins_dir}.{plugin_name}.routes'
        try:
            module = importlib.import_module(routes_module)
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp)
            description = getattr(module, 'PLUGIN_DESCRIPTION', '无描述')
            result['plugins'].append({'name': plugin_name, 'description': description})
            result['success'] += 1
        except Exception as e:
            result['failed'] += 1
            continue
    return result