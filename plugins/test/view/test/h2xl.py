import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from .utils import load_font, text_size, draw_centered_text, draw_color_strip, draw_grid


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    img, draw = create_canvas("h2xl", palette_type="bw", cmode=cmode)
    W, H = img.width, img.height

    font32 = load_font(32)
    font16 = load_font(16)

    margin = 16

    draw.rectangle([(margin, margin), (W - margin, H - margin)], outline=1, width=1)

    draw_centered_text(draw, W // 2, margin + 12, "TEST h2xl", fill=1, font=font32, img_width=W, img_height=H)
    _, th = text_size(draw, "TEST h2xl", font32)

    draw_centered_text(draw, W // 2, margin + 12 + th + 6, "400 x 300", fill=1, font=font16, img_width=W, img_height=H)
    _, th2 = text_size(draw, "400 x 300", font16)

    grid_x = margin + 12
    grid_y = margin + 12 + th + 6 + th2 + 20
    grid_w = W - margin * 2 - 24
    grid_h = H - grid_y - margin - 52
    draw_grid(draw, grid_x, grid_y, grid_w, grid_h, 5, 4, fill=1, width=1)

    strip_y = H - margin - 28
    strip_h = 20
    draw_color_strip(draw, margin + 12, strip_y, W - margin * 2 - 24, strip_h, [0, 1])

    label_y = strip_y - 22
    draw_centered_text(draw, W // 2, label_y, "BW Palette", fill=1, font=font16, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)