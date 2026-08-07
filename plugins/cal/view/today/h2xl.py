import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.cal_data import get_today_data
from .utils import load_font, text_size, draw_safe_text, draw_separator


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    tz = kwargs.get("tz")
    data = get_today_data(tz=tz)

    img, draw = create_canvas("h2xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    title_font = load_font(32)
    body_font = load_font(16)

    solar_str = "{}年{}月{}日".format(
        data["solar_year"], data["solar_month"], data["solar_day"]
    )
    weekday_str = data["weekday"]
    lunar_str = "{}{}".format(data["lunar_month_name"], data["lunar_day_name"])
    ganzhi_str = "{} {} {}".format(
        data["year_ganzhi"], data["month_ganzhi"], data["day_ganzhi"]
    )
    shengxiao_str = "{}年".format(data["shengxiao"])
    jieqi_str = data["jieqi"]

    cx = 20
    cy = 12

    draw_safe_text(draw, (cx, cy), solar_str, fill=2, font=title_font, img_width=W, img_height=H)
    solar_tw, solar_th = text_size(draw, solar_str, title_font)

    cy += solar_th + 8
    draw_safe_text(draw, (cx, cy), weekday_str, fill=1, font=body_font, img_width=W, img_height=H)
    _, wd_th = text_size(draw, weekday_str, body_font)

    cy += wd_th + 12
    draw_safe_text(draw, (cx, cy), lunar_str, fill=1, font=title_font, img_width=W, img_height=H)
    _, lunar_th = text_size(draw, lunar_str, title_font)

    cy += lunar_th + 12
    draw_safe_text(draw, (cx, cy), ganzhi_str, fill=1, font=body_font, img_width=W, img_height=H)
    _, gz_th = text_size(draw, ganzhi_str, body_font)

    cy += gz_th + 8
    draw_safe_text(draw, (cx, cy), shengxiao_str, fill=1, font=body_font, img_width=W, img_height=H)
    _, sx_th = text_size(draw, shengxiao_str, body_font)

    cy += sx_th + 8
    draw_separator(draw, cy, W)
    cy += 10

    if jieqi_str:
        draw_safe_text(draw, (cx, cy), "节气: {}".format(jieqi_str), fill=2, font=body_font, img_width=W, img_height=H)
        _, jq_th = text_size(draw, "节气: {}".format(jieqi_str), body_font)
        cy += jq_th + 4

    festivals = data["festivals"] + data["other_festivals"]
    if festivals:
        fest_str = "节日: {}".format(" · ".join(festivals[:4]))
        draw_safe_text(draw, (cx, cy), fest_str, fill=2, font=body_font, img_width=W, img_height=H)
        _, fest_th = text_size(draw, fest_str, body_font)
        cy += fest_th + 4

    cy += 4
    draw_separator(draw, cy, W)
    cy += 10

    yi_list = data["yi"]
    ji_list = data["ji"]
    if yi_list:
        yi_str = "宜: {}".format(" ".join(yi_list[:6]))
        draw_safe_text(draw, (cx, cy), yi_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, yi_th = text_size(draw, yi_str, body_font)
        cy += yi_th + 4
    if ji_list:
        ji_str = "忌: {}".format(" ".join(ji_list[:6]))
        draw_safe_text(draw, (cx, cy), ji_str, fill=1, font=body_font, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)