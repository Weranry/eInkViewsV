import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib
from datetime import datetime

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.cal_data import get_month_data
from .utils import (
    load_font, text_size, draw_safe_text, draw_centered_text, WEEKDAY_NAMES
)


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    today = datetime.now()
    data = get_month_data(today.year, today.month)

    img, draw = create_canvas("h2xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    title_font = load_font(32)
    day_font = load_font(16)

    margin_l = 20
    margin_r = 20
    grid_w = W - margin_l - margin_r
    col_w = grid_w // 7
    cols = 7

    title_str = "{}年{}月".format(data["year"], data["month"])
    cy = 12
    draw_safe_text(draw, (margin_l, cy), title_str, fill=2, font=title_font, img_width=W, img_height=H)
    _, title_th = text_size(draw, title_str, title_font)

    cy += title_th + 8
    for i, wd in enumerate(WEEKDAY_NAMES):
        cx = margin_l + i * col_w + col_w // 2
        fill = 2 if i in (0, 6) else 1
        draw_centered_text(draw, cx, cy, wd, fill=fill, font=day_font, img_width=W, img_height=H)
    _, wd_th = text_size(draw, WEEKDAY_NAMES[0], day_font)

    cy += wd_th + 8

    offset = data["first_weekday_offset"]
    row_h = (H - cy - 8) // 6
    lunar_font = load_font(16)

    for row in range(6):
        row_y = cy + row * row_h
        for col in range(cols):
            day_idx = row * cols + col - offset + 1
            if day_idx < 1 or day_idx > data["total_days"]:
                continue

            day_data = data["days"][day_idx - 1]
            cell_cx = margin_l + col * col_w + col_w // 2

            if day_data["is_today"]:
                solar_fill = 2
                lunar_fill = 2
            elif day_data["is_weekend"]:
                solar_fill = 2
                lunar_fill = 1
            else:
                solar_fill = 1
                lunar_fill = 1

            solar_str = str(day_data["solar_day"])
            lunar_str = day_data["lunar_day_name"]

            if day_data["jieqi"]:
                lunar_str = day_data["jieqi"]
                lunar_fill = 2

            solar_y = row_y + 4
            lunar_y = row_y + row_h - 4 - lunar_font.size

            draw_centered_text(
                draw, cell_cx, solar_y, solar_str,
                fill=solar_fill, font=day_font, img_width=W, img_height=H
            )
            draw_centered_text(
                draw, cell_cx, lunar_y, lunar_str,
                fill=lunar_fill, font=lunar_font, img_width=W, img_height=H
            )

    return finalize_image_common(img, rotate=rotate, invert=invert)