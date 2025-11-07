import io
import hashlib
import os
import importlib
from flask import Blueprint, request, send_file, make_response
from modules.errors.errors import ParamError
from config import DEFAULT_IMAGE_QUALITY
from modules.plugins import load_plugin_config

bp_random = Blueprint('random_views', __name__)

def parse_routes_param(param):
    if not param:
        raise ParamError('routes参数不能为空')
    items = []
    parts = param.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        segs = part.split(':')
        if len(segs) < 2:
            continue
        view_path = segs[0]
        size = segs[1]
        weight = 1.0
        param_dict = {}
        param_start = 2
        if len(segs) > 2:
            if '=' not in segs[2]:
                try:
                    weight = float(segs[2])
                    param_start = 3
                except ValueError:
                    param_start = 2
        for s in segs[param_start:]:
            if '=' in s:
                k, v = s.split('=', 1)
                param_dict[k] = v
        items.append(((view_path, size), weight, param_dict))
    filtered = [(vc, weight, param_dict) for vc, weight, param_dict in items if weight > 0]
    if not filtered:
        raise ParamError('所有权重均为0或未设置，无法选择视图')
    return filtered

@bp_random.route('/random/views')
def random_views():
    routes_param = request.args.get('routes')
    rotate_arg = request.args.get('rotate', None)
    invert_arg = request.args.get('invert', None)
    cmode_global = request.args.get('cmode', None)
    if not routes_param:
        raise ParamError('缺少 routes 参数')
    rotate_map = {'c': 270, 'cc': 90, 'h': 180}
    invert_map = {'t': True, 'f': False}
    global_rotate = rotate_map.get(rotate_arg, None)
    global_invert = invert_map.get(invert_arg, None)
    choices = parse_routes_param(routes_param)
    view_size_pairs = [vc for vc, _, _ in choices]
    weights = [weight for _, weight, _ in choices]
    params_list = [param_dict for _, _, param_dict in choices]
    try:
        import random
        idx = random.choices(range(len(view_size_pairs)), weights=weights, k=1)[0]
        (view_path, size) = view_size_pairs[idx]
        params = params_list[idx]
        plugin, kind = view_path.split('.', 1)
        mod_path = f'plugins.{plugin}.view.{kind}.{size}'
        mod = importlib.import_module(mod_path)
        plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../plugins/{plugin}'))
        plugin_config = load_plugin_config(plugin, plugin_dir)
        plugin_default_args = plugin_config.get('DEFAULT_ARGS', {}) if 'DEFAULT_ARGS' in plugin_config else {}
        plugin_default_rotate = plugin_config.get('DEFAULT_ROTATE', None)
        plugin_default_invert = plugin_config.get('DEFAULT_INVERT', None)
        extra_params = dict(plugin_default_args)
        extra_params.update(params)
        extra_params.pop('rotate', None)
        extra_params.pop('invert', None)
        cmode = params.get('cmode', cmode_global if cmode_global is not None else plugin_default_args.get('cmode', None))
        rotate_val = params.get('rotate', None)
        if rotate_val is not None:
            rotate = rotate_map.get(rotate_val, 0)
        elif global_rotate is not None:
            rotate = global_rotate
        elif plugin_default_rotate is not None:
            rotate = plugin_default_rotate
        else:
            from config import DEFAULT_ROTATE
            rotate = DEFAULT_ROTATE
        invert_val = params.get('invert', None)
        if invert_val is not None:
            invert = invert_map.get(invert_val, False)
        elif global_invert is not None:
            invert = global_invert
        elif plugin_default_invert is not None:
            invert = plugin_default_invert
        else:
            from config import DEFAULT_INVERT
            invert = DEFAULT_INVERT
    except Exception as e:
        raise ParamError(f'随机图片生成失败: {str(e)}')
    if not hasattr(mod, 'generate_image'):
        raise ParamError(f'视图 {mod_path} 未实现 generate_image')
    try:
        img = mod.generate_image(rotate=rotate, invert=invert, cmode=cmode, **extra_params)
    except Exception as e:
        raise ParamError(f'随机图片生成失败: {str(e)}')
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=DEFAULT_IMAGE_QUALITY, subsampling=0, progressive=False)
    buf.seek(0)
    filename = f"{plugin}_{kind}_{size}.jpg"
    response = make_response(send_file(buf, mimetype='image/jpeg', download_name=filename))
    return response