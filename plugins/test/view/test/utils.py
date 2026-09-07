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


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), str(text), font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_text(draw, cx, y, text, fill, font, img_width, img_height):
    text = str(text)
    tw, th = text_size(draw, text, font)
    x = cx - tw // 2
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x + tw > img_width:
        x = max(0, img_width - tw - 2)
    if y + th > img_height:
        y = max(0, img_height - th - 2)
    draw.text((x, y), text, fill=fill, font=font)
    return tw, th


def draw_grid(draw, x, y, w, h, cols, rows, fill=1, width=1):
    cell_w = w // cols
    cell_h = h // rows
    for i in range(cols + 1):
        lx = x + i * cell_w
        draw.line([(lx, y), (lx, y + h)], fill=fill, width=width)
    for j in range(rows + 1):
        ly = y + j * cell_h
        draw.line([(x, ly), (x + w, ly)], fill=fill, width=width)


def draw_color_strip(draw, x, y, w, h, colors):
    n = len(colors)
    if n == 0:
        return
    strip_w = w // n
    for i, color in enumerate(colors):
        sx = x + i * strip_w
        draw.rectangle([(sx, y), (sx + strip_w, y + h)], fill=color)