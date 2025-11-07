import importlib
import os
from flask import Flask
import sys
import time

def register_plugins(app: Flask, plugins_dir='plugins'):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    plugin_names = [
        name for name in os.listdir(plugins_dir)
        if os.path.isdir(os.path.join(plugins_dir, name)) and os.path.exists(os.path.join(plugins_dir, name, 'routes.py'))
    ]
    total = len(plugin_names)
    success = 0
    failed = 0
    if not plugin_names:
        return
    for plugin_name in plugin_names:
        routes_module = f'{plugins_dir}.{plugin_name}.routes'
        try:
            start = time.time()
            module = importlib.import_module(routes_module)
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp)
            plugin_description = getattr(module, 'PLUGIN_DESCRIPTION', None)
            if not plugin_description:
                plugin_description = '无描述'
            elapsed = time.time() - start
            success += 1
        except Exception as e:
            failed += 1
            continue
