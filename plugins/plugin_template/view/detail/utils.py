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


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), str(text), font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_panel(draw, x, y, width, title, body, title_font, body_font):
    draw.text((x, y), str(title), fill=2, font=title_font)
    title_h = text_size(draw, title, title_font)[1]
    draw.text((x, y + title_h + 6), str(body), fill=1, font=body_font)
    body_h = text_size(draw, body, body_font)[1]
    return title_h + 6 + body_h
