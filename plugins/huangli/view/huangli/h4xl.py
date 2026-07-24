import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.huangli_data import get_huangli_data
from .utils import (
    load_font, text_size, draw_safe_text,
    draw_h_line, draw_box, truncate_text,
)


def _draw_cell(draw, x, y, w, h, title, items, title_font, body_font, img_w, img_h):
    draw_box(draw, x, y, x + w, y + h, fill=1, width=1)
    title_tw, title_th = text_size(draw, title, title_font)
    title_cx = x + w // 2
    title_x = title_cx - title_tw // 2
    draw_safe_text(draw, (title_x, y + 4), title, fill=1, font=title_font, img_width=img_w, img_height=img_h)
    draw_h_line(draw, y + title_th + 6, x + 2, x + w - 2, fill=1, width=1)

    item_y = y + title_th + 10
    max_items = 4
    max_item_w = w - 12
    for i, item in enumerate(items[:max_items]):
        if item_y + 18 > y + h - 2:
            break
        item_text = truncate_text(draw, item, body_font, max_item_w)
        if not item_text:
            break
        draw_safe_text(draw, (x + 6, item_y), item_text, fill=1, font=body_font, img_width=img_w, img_height=img_h)
        _, item_th = text_size(draw, item_text, body_font)
        item_y += item_th + 2


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    data = get_huangli_data()

    img, draw = create_canvas("h4xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    title_font = load_font(32)
    body_font = load_font(16)

    margin = 24
    cell_gap = 10
    cell_w = 242
    x1 = margin
    x2 = margin + cell_w + cell_gap
    x3 = margin + (cell_w + cell_gap) * 2

    cy = 10

    solar_str = "{}年{}月{}日 星期{}".format(
        data["solar_year"], data["solar_month"], data["solar_day"], data["weekday"]
    )
    draw_safe_text(draw, (margin, cy), solar_str, fill=1, font=title_font, img_width=W, img_height=H)
    _, th = text_size(draw, solar_str, title_font)
    cy += th + 4

    lunar_str = "农历 {}年 {}月 {}".format(
        data["year_ganzhi"], data["lunar_month_name"], data["lunar_day_name"]
    )
    draw_safe_text(draw, (margin, cy), lunar_str, fill=1, font=title_font, img_width=W, img_height=H)
    _, th = text_size(draw, lunar_str, title_font)
    cy += th + 4

    ganzhi_str = "干支: {}年 {}月 {}日".format(
        data["year_ganzhi"], data["month_ganzhi"], data["day_ganzhi"]
    )
    nayin_str = ""
    if data["nayin_day"]:
        nayin_str = "  纳音: {}".format(data["nayin_day"])
    line3 = "{}{}  生肖: {}".format(ganzhi_str, nayin_str, data["shengxiao"])
    draw_safe_text(draw, (margin, cy), line3, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, line3, body_font)
    cy += th + 2

    extra_parts = []
    if data["jieqi"]:
        extra_parts.append("节气: {}".format(data["jieqi"]))
    all_festivals = data["festivals"] + data["other_festivals"]
    if all_festivals:
        extra_parts.append("节日: {}".format(" · ".join(all_festivals[:3])))
    if extra_parts:
        extra_str = "  |  ".join(extra_parts)
        draw_safe_text(draw, (margin, cy), extra_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, extra_str, body_font)
        cy += th + 2

    cy += 6
    draw_h_line(draw, cy, margin, W - margin, fill=1, width=1)
    cy += 8

    grid_top = cy
    cell_h = 136
    row1_y = grid_top
    row2_y = grid_top + cell_h + cell_gap

    _draw_cell(draw, x1, row1_y, cell_w, cell_h,
               "宜", data["yi"], title_font, body_font, W, H)
    _draw_cell(draw, x2, row1_y, cell_w, cell_h,
               "忌", data["ji"], title_font, body_font, W, H)
    _draw_cell(draw, x3, row1_y, cell_w, cell_h,
               "吉神宜趋", data["jishen"], title_font, body_font, W, H)

    _draw_cell(draw, x1, row2_y, cell_w, cell_h,
               "凶煞宜忌", data["xiongsha"], title_font, body_font, W, H)

    chong_items = []
    if data["chong_desc"]:
        chong_items.append(data["chong_desc"])
    if data["sha"]:
        chong_items.append("煞{}".format(data["sha"]))
    _draw_cell(draw, x2, row2_y, cell_w, cell_h,
               "冲煞", chong_items, title_font, body_font, W, H)

    pengzu_items = []
    if data["pengzu_gan"]:
        pengzu_items.append(data["pengzu_gan"])
    if data["pengzu_zhi"]:
        pengzu_items.append(data["pengzu_zhi"])
    _draw_cell(draw, x3, row2_y, cell_w, cell_h,
               "彭祖百忌", pengzu_items, title_font, body_font, W, H)

    bottom_y = row2_y + cell_h + 8
    draw_h_line(draw, bottom_y, margin, W - margin, fill=1, width=1)
    bottom_y += 8

    bottom_parts = []
    if data["zhixing"]:
        bottom_parts.append("值星: {}".format(data["zhixing"]))
    if data["xiu"]:
        xiu_info = "二十八宿: {}".format(data["xiu"])
        if data["xiu_luck"]:
            xiu_info += "({})".format(data["xiu_luck"])
        bottom_parts.append(xiu_info)
    if data["liuyao"]:
        bottom_parts.append("六曜: {}".format(data["liuyao"]))

    bottom_line1 = "  |  ".join(bottom_parts)
    if bottom_line1:
        draw_safe_text(draw, (margin, bottom_y), bottom_line1, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, bottom_line1, body_font)
        bottom_y += th + 2

    pos_parts = []
    if data["pos_xi"]:
        pos_parts.append("喜神: {}".format(data["pos_xi"]))
    if data["pos_fu"]:
        pos_parts.append("福神: {}".format(data["pos_fu"]))
    if data["pos_cai"]:
        pos_parts.append("财神: {}".format(data["pos_cai"]))
    if data["day_lu"]:
        pos_parts.append("日禄: {}".format(data["day_lu"]))

    bottom_line2 = "  |  ".join(pos_parts)
    if bottom_line2:
        draw_safe_text(draw, (margin, bottom_y), bottom_line2, fill=1, font=body_font, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)