from plugins.steam.lib.fetcher import fetch_steam_data
from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from plugins.steam.view.stats.utils import render_steam_stats
from modules.errors.errors import ParamError

def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    api_key = kwargs.get('api_key')
    steam_id = kwargs.get('steam_id')

    if not api_key or not steam_id:
        raise ParamError("Missing mandatory parameters: api_key, steam_id")

    data = fetch_steam_data(api_key, steam_id)

    size_key = kwargs.get('size', 'v2xl')
    canvas, draw = create_canvas(size_key, 'bwr', cmode=cmode)

    # 渲染动态 Grid 网格视图
    render_steam_stats(canvas, draw, data)

    return finalize_image_common(canvas, rotate=rotate, invert=invert)