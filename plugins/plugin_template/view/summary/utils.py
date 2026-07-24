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


def draw_label_value(draw, x, y, label, value, label_font, value_font, label_fill=2, value_fill=1, gap=6):
    draw.text((x, y), str(label), fill=label_fill, font=label_font)
    label_w, label_h = text_size(draw, label, label_font)
    draw.text((x + label_w + gap, y), str(value), fill=value_fill, font=value_font)
    value_h = text_size(draw, value, value_font)[1]
    return max(label_h, value_h)


def draw_rows(draw, x, y, rows, label_font, value_font, row_gap=8):
    current_y = y
    for label, value in rows:
        row_h = draw_label_value(draw, x, current_y, label, value, label_font, value_font)
        current_y += row_h + row_gap
    return current_y
