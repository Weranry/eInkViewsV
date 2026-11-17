"""astro 视图公共工具：时区解析、月相取数、字体与排版辅助。

两个尺寸（hxl / h2xl）共用同一份取数与测量逻辑，尺寸文件里只留版式。
"""

import datetime

from modules.errors.errors import ParamError
from modules.generate_views.font_loader import get_font, get_root_font_path
from modules.utils.timezone import convert_utc_to_local, now_in_timezone
from ...lib.moon_calc import calc_moon_phase

FONT_PATH = get_root_font_path('font.ttf')


def load_font(size):
    """按字号加载根字体；字号须为 16 的整数倍。"""
    return get_font(size, FONT_PATH)


def get_moon_data(tz=None, lat=None, lon=None):
    """解析经纬度并算出当地当前时刻的月相数据。

    返回 (now, moon_data, lat, lon)。经纬度必须成对提供。

    相位只取决于绝对时刻，故按 UTC 计算；展示用的 `now` 与两个月相时刻则换算到本地时区。
    """
    if lat is not None and lon is None:
        raise ParamError('lon 参数缺失，经纬度需同时提供')
    if lon is not None and lat is None:
        raise ParamError('lat 参数缺失，经纬度需同时提供')

    lat = float(lat) if lat else 0.0
    lon = float(lon) if lon else 0.0

    moon = calc_moon_phase(datetime.datetime.now(datetime.timezone.utc), lat=lat)
    moon['next_new_moon'] = convert_utc_to_local(moon['next_new_moon'], tz)
    moon['next_full_moon'] = convert_utc_to_local(moon['next_full_moon'], tz)
    return now_in_timezone(tz), moon, lat, lon


def wrap_by_space(text, font, max_width, max_lines=2):
    """按空格折行，最多 max_lines 行。

    英文相位名（如 Waxing Crescent）在窄栏里放不下时拆成两行，
    避免超出画布被裁掉。字号固定，不靠缩字号来塞进一行。
    """
    words = text.split()
    lines, current = [], ''
    for word in words:
        candidate = f'{current} {word}'.strip()
        if not current or font.getlength(candidate) <= max_width:
            current = candidate
        else:
            lines.append(current)
            if len(lines) >= max_lines:
                return lines[:max_lines]
            current = word
    if current:
        lines.append(current)
    return lines[:max_lines]