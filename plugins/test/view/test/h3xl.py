import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from .utils import load_font, text_size, draw_centered_text, draw_color_strip, draw_grid


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    img, draw = create_canvas("h3xl", palette_type="bw", cmode=cmode)
    W, H = img.width, img.height

    font48 = load_font(48)
    font32 = load_font(32)
    font16 = load_font(16)

    margin = 24

    draw.rectangle([(margin, margin), (W - margin, H - margin)], outline=1, width=1)

    draw_centered_text(draw, W // 2, margin + 16, "TEST h3xl", fill=1, font=font48, img_width=W, img_height=H)
    _, th = text_size(draw, "TEST h3xl", font48)

    draw_centered_text(draw, W // 2, margin + 16 + th + 8, "600 x 480", fill=1, font=font32, img_width=W, img_height=H)
    _, th2 = text_size(draw, "600 x 480", font32)

    draw_centered_text(draw, W // 2, margin + 16 + th + 8 + th2 + 8, "eInkViews Test Pattern", fill=1, font=font16, img_width=W, img_height=H)
    _, th3 = text_size(draw, "eInkViews Test Pattern", font16)

    grid_x = margin + 16
    grid_y = margin + 16 + th + 8 + th2 + 8 + th3 + 24
    grid_w = W - margin * 2 - 32
    grid_h = H - grid_y - margin - 64
    draw_grid(draw, grid_x, grid_y, grid_w, grid_h, 8, 5, fill=1, width=1)

    strip_y = H - margin - 32
    strip_h = 24
    draw_color_strip(draw, margin + 16, strip_y, W - margin * 2 - 32, strip_h, [0, 1])

    label_y = strip_y - 28
    draw_centered_text(draw, W // 2, label_y, "BW Palette  |  White / Black", fill=1, font=font16, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)