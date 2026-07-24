from PIL import ImageFont
import importlib

font_loader = importlib.import_module("modules.generate_views.font_loader")
get_root_font_path = font_loader.get_root_font_path
get_font = font_loader.get_font

from ...lib.weather_icons import get_weather_icon


def wind_direction_text(degrees):
    if degrees is None:
        return "N/A"
    directions = [
        "北", "东北偏北", "东北", "东北偏东",
        "东", "东南偏东", "东南", "东南偏南",
        "南", "西南偏南", "西南", "西南偏西",
        "西", "西北偏西", "西北", "西北偏北",
    ]
    idx = int((degrees + 11.25) / 22.5) % 16
    return directions[idx]


def load_font(size):
    try:
        return get_font(size, get_root_font_path("font.ttf"))
    except Exception:
        return ImageFont.load_default()


def load_icon_font(size):
    try:
        return get_font(size, get_root_font_path("weather-icon.ttf"))
    except Exception:
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