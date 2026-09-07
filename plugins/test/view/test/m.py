import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from .utils import load_font, text_size, draw_centered_text, draw_color_strip, draw_grid


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    img, draw = create_canvas("m", palette_type="bw", cmode=cmode)
    W, H = img.width, img.height

    font32 = load_font(32)
    font16 = load_font(16)

    margin = 8

    draw.rectangle([(margin, margin), (W - margin, H - margin)], outline=1, width=1)

    draw_centered_text(draw, W // 2, margin + 6, "TEST m", fill=1, font=font32, img_width=W, img_height=H)
    _, th = text_size(draw, "TEST m", font32)

    draw_centered_text(draw, W // 2, margin + 6 + th + 4, "200 x 200", fill=1, font=font16, img_width=W, img_height=H)

    grid_x = margin + 4
    grid_y = margin + 6 + th + 4 + 20 + 12
    grid_w = W - margin * 2 - 8
    grid_h = 80
    draw_grid(draw, grid_x, grid_y, grid_w, grid_h, 4, 4, fill=1, width=1)

    strip_y = grid_y + grid_h + 12
    strip_h = 20
    draw_color_strip(draw, margin + 4, strip_y, W - margin * 2 - 8, strip_h, [0, 1])

    return finalize_image_common(img, rotate=rotate, invert=invert)