import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from .utils import load_font, text_size, draw_centered_text, draw_color_strip, draw_grid


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    img, draw = create_canvas("hxl", palette_type="bw", cmode=cmode)
    W, H = img.width, img.height

    font32 = load_font(32)
    font16 = load_font(16)

    margin = 12

    draw.rectangle([(margin, margin), (W - margin, H - margin)], outline=1, width=1)

    draw_centered_text(draw, W // 4, margin + 8, "TEST hxl", fill=1, font=font32, img_width=W, img_height=H)
    _, th = text_size(draw, "TEST hxl", font32)
    draw_centered_text(draw, W // 4, margin + 8 + th + 4, "384 x 184", fill=1, font=font16, img_width=W, img_height=H)

    grid_x = W // 2 + 8
    grid_y = margin + 8
    grid_w = W // 2 - margin - 16
    grid_h = H - margin * 2 - 16 - 32
    draw_grid(draw, grid_x, grid_y, grid_w, grid_h, 6, 4, fill=1, width=1)

    strip_y = H - margin - 24
    strip_h = 16
    draw_color_strip(draw, margin + 4, strip_y, W // 2 - 12, strip_h, [0, 1])

    return finalize_image_common(img, rotate=rotate, invert=invert)