import importlib
import os
from flask import request, jsonify, abort
from modules.errors.errors import ParamError
from modules.plugins import load_plugin_config

def register_json_routes(bp, plugin_name, json_module_dir):
    if not os.path.exists(json_module_dir):
        return
    plugin_dir = os.path.dirname(json_module_dir)
    plugin_config = load_plugin_config(plugin_name, plugin_dir)
    for fname in os.listdir(json_module_dir):
        if fname.endswith('.py') and not fname.startswith('_'):
            json_name = fname[:-3]
            def make_json_func(json_name=json_name, fname=fname):
                def json_func():
                    mod_path = f'plugins.{plugin_name}.json_module.{json_name}'
                    try:
                        mod = importlib.import_module(mod_path)
                    except Exception:
                        raise ParamError(f'JSON模块 {mod_path} 不存在')
                    if not hasattr(mod, 'to_json'):
                        raise ParamError(f'JSON模块 {mod_path} 未实现 to_json')
                    req_args = dict(request.args)
                    merged_args = dict(plugin_config.get('DEFAULT_ARGS', {}))
                    merged_args.update(req_args)
                    try:
                        result = mod.to_json(**merged_args)
                    except Exception as e:
                        raise ParamError(f'JSON数据生成失败: {str(e)}')
                    return jsonify(result)
                json_func.__name__ = f'json_{plugin_name}_{json_name}'
                return json_func
            bp.add_url_rule(f'/{plugin_name}/json/{json_name}', view_func=make_json_func())
