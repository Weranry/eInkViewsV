import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.weather_data import fetch_current_weather
from ...lib.weather_icons import get_weather_icon
from .utils import (
    wind_direction_text,
    load_font, load_icon_font, text_size,
    draw_safe_text, draw_separator,
)


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    data = fetch_current_weather(lat, lon, tz)

    img, draw = create_canvas("hxl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    temp = data["temperature"]
    feels = data["feels_like"]
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    wind_dir = data["wind_direction"]
    pressure = data["pressure"]
    weather_code = data["weather_code"]
    weather_icon, weather_desc = get_weather_icon(weather_code)

    temp_str = f"{temp:.0f}" if temp is not None else "--"
    feels_str = f"{feels:.0f}" if feels is not None else "--"
    humidity_str = f"{humidity:.0f}%" if humidity is not None else "--"
    wind_str = f"{wind_speed:.1f} m/s" if wind_speed is not None else "--"
    pressure_str = f"{pressure:.0f} hPa" if pressure is not None else "--"
    wind_dir_str = wind_direction_text(wind_dir)

    icon_font = load_icon_font(48)
    title_font = load_font(32)
    body_font = load_font(16)
    temp_font = load_font(48)

    icon_char = weather_icon
    icon_tw, icon_th = text_size(draw, icon_char, icon_font)
    draw_safe_text(draw, (16, 8), icon_char, fill=1, font=icon_font, img_width=W, img_height=H)

    temp_text = f"{temp_str}"
    temp_tw, temp_th = text_size(draw, temp_text, temp_font)
    draw_safe_text(draw, (W - 16 - temp_tw, 8), temp_text, fill=2, font=temp_font, img_width=W, img_height=H)

    unit_text = ""
    draw_safe_text(draw, (W - 16 - 20, 8 + temp_th), unit_text, fill=1, font=body_font, img_width=W, img_height=H)

    desc_y = 8 + max(icon_th, temp_th) + 10
    desc_text = weather_desc
    draw_safe_text(draw, (16, desc_y), desc_text, fill=1, font=title_font, img_width=W, img_height=H)

    feels_y = desc_y + 36
    feels_text = f"TI {feels_str}"
    draw_safe_text(draw, (16, feels_y), feels_text, fill=1, font=body_font, img_width=W, img_height=H)

    sep_y = feels_y + 24
    draw_separator(draw, sep_y, W)

    detail_y = sep_y + 8
    detail_font = load_font(16)

    h_text = f"RH {humidity_str}"
    draw_safe_text(draw, (16, detail_y), h_text, fill=1, font=detail_font, img_width=W, img_height=H)

    w_text = f"WIND {wind_str} {wind_dir_str}"
    draw_safe_text(draw, (16, detail_y + 22), w_text, fill=1, font=detail_font, img_width=W, img_height=H)

    p_text = f"P {pressure_str}"
    draw_safe_text(draw, (16, detail_y + 44), p_text, fill=1, font=detail_font, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)