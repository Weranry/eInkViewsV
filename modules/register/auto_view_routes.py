import io
import hashlib
import importlib
from flask import send_file, request, make_response, abort
from modules.errors.errors import ParamError
from config import DEFAULT_IMAGE_QUALITY, DEFAULT_ROTATE, DEFAULT_INVERT
from modules.plugins import load_plugin_config
import os

def register_view_routes(bp, plugin_name, view_dir):
    plugin_dir = os.path.dirname(view_dir)
    plugin_config = load_plugin_config(plugin_name, plugin_dir)
    plugin_default_args = plugin_config.get('DEFAULT_ARGS', {}) if 'DEFAULT_ARGS' in plugin_config else {}
    plugin_default_rotate = plugin_config.get('DEFAULT_ROTATE', None)
    plugin_default_invert = plugin_config.get('DEFAULT_INVERT', None)
    for kind in os.listdir(view_dir):
        kind_path = os.path.join(view_dir, kind)
        if not os.path.isdir(kind_path):
            continue
        def make_view_func(kind=kind):
            def view_func():
                size = request.args.get('size')
                if not size:
                    raise ParamError('缺少 size 参数')
                try:
                    mod = importlib.import_module(f'plugins.{plugin_name}.view.{kind}.{size}')
                except ModuleNotFoundError:
                    raise ParamError(f'视图 {plugin_name}.view.{kind}.{size} 不存在')
                if not hasattr(mod, 'generate_image'):
                    raise ParamError(f'视图 {plugin_name}.view.{kind}.{size} 未实现 generate_image')
                req_args = dict(request.args)
                merged_args = dict(plugin_default_args)
                cmode = req_args.get('cmode', plugin_default_args.get('cmode', None))
                rotate_arg = req_args.get('rotate')
                if rotate_arg is not None:
                    rotate_map = {'c': 270, 'cc': 90, 'h': 180}
                    rotate = rotate_map.get(rotate_arg, 0)
                elif plugin_default_rotate is not None:
                    rotate = plugin_default_rotate
                else:
                    rotate = DEFAULT_ROTATE
                invert_arg = req_args.get('invert')
                invert_map = {'t': True, 'f': False}
                if invert_arg is not None:
                    try:
                        invert = invert_map[invert_arg]
                    except KeyError:
                        raise ParamError('invert 参数必须为 t 或 f')
                elif plugin_default_invert is not None:
                    invert = plugin_default_invert
                else:
                    invert = DEFAULT_INVERT
                try:
                    img = mod.generate_image(rotate=rotate, invert=invert, cmode=cmode, **merged_args)
                except Exception as e:
                    raise ParamError(f'图片生成失败: {str(e)}')
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=DEFAULT_IMAGE_QUALITY, subsampling=0, progressive=False)
                buf.seek(0)
                filename = f"{plugin_name}_{kind}_{size}.jpg"
                response = make_response(send_file(buf, mimetype='image/jpeg', download_name=filename))
                return response
            view_func.__name__ = f'view_{plugin_name}_{kind}'
            return view_func
        bp.add_url_rule(f'/{plugin_name}/view/{kind}', view_func=make_view_func())