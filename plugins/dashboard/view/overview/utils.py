from PIL import ImageFont
import importlib

font_loader = importlib.import_module("modules.generate_views.font_loader")
get_root_font_path = font_loader.get_root_font_path
get_font = font_loader.get_font


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


def draw_h_line(draw, y, x1, x2, fill=1, width=1):
    draw.line([(x1, y), (x2, y)], fill=fill, width=width)


def draw_v_line(draw, x, y1, y2, fill=1, width=1):
    draw.line([(x, y1), (x, y2)], fill=fill, width=width)


def wrap_text(draw, text, font, max_width):
    if not text:
        return []
    lines = []
    current_line = ""
    for ch in text:
        test_line = current_line + ch
        tw, _ = text_size(draw, test_line, font)
        if tw > max_width:
            if current_line:
                lines.append(current_line)
            current_line = ch
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def truncate_text(draw, text, font, max_width):
    if not text:
        return ""
    result = ""
    for ch in text:
        test = result + ch
        tw, _ = text_size(draw, test, font)
        if tw > max_width:
            return result
        result = test
    return result