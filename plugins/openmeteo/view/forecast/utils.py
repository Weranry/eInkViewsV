import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

font_loader = importlib.import_module("modules.generate_views.font_loader")
get_root_font_path = font_loader.get_root_font_path
get_font = font_loader.get_font


def load_font(size):
    try:
        return get_font(size, get_root_font_path("font.ttf"))
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


def load_icon_font(size):
    try:
        return get_font(size, get_root_font_path("weather-icon.ttf"))
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), str(text), font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_safe_text(draw, xy, text, fill, font, img_width, img_height):
    x, y = xy
    text = str(text)
    tw, th = text_size(draw, text, font)
    if x + tw > img_width:
        x = max(0, img_width - tw - 2)
    if y + th > img_height:
        y = max(0, img_height - th - 2)
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    draw.text((x, y), text, fill=fill, font=font)
    return tw, th


def draw_separator(draw, y, img_width):
    draw.line([(16, y), (img_width - 16, y)], fill=1, width=1)


WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def date_to_weekday(date_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return WEEKDAY_NAMES[dt.weekday()]
    except Exception:
        return date_str


def draw_forecast_column(draw, x, y, col_w, day_data, day_font, icon_font, temp_font, W, H):
    from ...lib.weather_icons import get_weather_icon

    icon, desc = get_weather_icon(day_data["weather_code"])
    day_label = date_to_weekday(day_data["date"])
    t_max = day_data["temp_max"]
    t_min = day_data["temp_min"]
    precip = day_data["precip_prob"]

    center_x = x + col_w // 2

    day_tw, day_th = text_size(draw, day_label, day_font)
    draw_safe_text(draw, (center_x - day_tw // 2, y), day_label, fill=1, font=day_font, img_width=W, img_height=H)

    icon_y = y + day_th + 4
    icon_tw, icon_th = text_size(draw, icon, icon_font)
    draw_safe_text(draw, (center_x - icon_tw // 2, icon_y), icon, fill=1, font=icon_font, img_width=W, img_height=H)

    temp_y = icon_y + icon_th + 4
    t_max_str = f"{t_max:.0f}" if t_max is not None else "--"
    t_min_str = f"{t_min:.0f}" if t_min is not None else "--"
    temp_text = f"{t_max_str}/{t_min_str}"
    temp_tw, temp_th = text_size(draw, temp_text, temp_font)
    draw_safe_text(draw, (center_x - temp_tw // 2, temp_y), temp_text, fill=1, font=temp_font, img_width=W, img_height=H)

    if precip is not None:
        precip_y = temp_y + temp_th + 2
        precip_text = f"{precip:.0f}%"
        precip_tw, precip_th = text_size(draw, precip_text, temp_font)
        draw_safe_text(draw, (center_x - precip_tw // 2, precip_y), precip_text, fill=2, font=temp_font, img_width=W, img_height=H)
        return precip_y + precip_th
    return temp_y + temp_th