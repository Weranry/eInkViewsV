import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.weather_data import fetch_daily_forecast
from .utils import (
    load_font, load_icon_font, text_size,
    draw_safe_text, draw_separator, draw_forecast_column,
)


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    forecast = fetch_daily_forecast(lat, lon, tz, days=5)

    img, draw = create_canvas("h2xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    title_font = load_font(32)
    day_font = load_font(16)
    icon_font = load_icon_font(32)
    temp_font = load_font(16)

    title_text = "预报"
    title_tw, title_th = text_size(draw, title_text, title_font)
    draw_safe_text(draw, (20, 12), title_text, fill=2, font=title_font, img_width=W, img_height=H)

    sep_y = 12 + title_th + 10
    draw_separator(draw, sep_y, W)

    col_w = (W - 40) // 5
    grid_y = sep_y + 12

    for i, day in enumerate(forecast[:5]):
        x = 20 + i * col_w
        draw_forecast_column(draw, x, grid_y, col_w, day, day_font, icon_font, temp_font, W, H)

    return finalize_image_common(img, rotate=rotate, invert=invert)