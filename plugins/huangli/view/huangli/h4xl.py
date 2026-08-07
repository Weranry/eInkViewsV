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
    draw_centered_text, draw_h_line, truncate_text,
)


def _draw_column_items(draw, x, y, col_w, items, font, img_w, img_h, max_items=5):
    item_y = y
    item_x = x + 4
    max_w = col_w - 8
    for item in items[:max_items]:
        if item_y + 22 > img_h - 4:
            break
        txt = truncate_text(draw, item, font, max_w)
        if not txt:
            continue
        draw_safe_text(draw, (item_x, item_y), txt, fill=1, font=font, img_width=img_w, img_height=img_h)
        _, th = text_size(draw, txt, font)
        item_y += th + 3


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    tz = kwargs.get("tz")
    data = get_huangli_data(tz=tz)

    img, draw = create_canvas("h4xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    font48 = load_font(48)
    font32 = load_font(32)
    font16 = load_font(16)

    margin = 24
    col_gap = 24
    col_w = (W - margin * 2 - col_gap * 2) // 3
    x1 = margin
    x2 = margin + col_w + col_gap
    x3 = margin + (col_w + col_gap) * 2
    cx = W // 2

    cy = 16

    solar_str = "{}年{}月{}日 星期{}".format(
        data["solar_year"], data["solar_month"], data["solar_day"], data["weekday"]
    )
    draw_centered_text(draw, cx, cy, solar_str, fill=1, font=font48, img_width=W, img_height=H)
    _, th = text_size(draw, solar_str, font48)
    cy += th + 4

    lunar_str = "农历 {}年 {}月 {}".format(
        data["year_ganzhi"], data["lunar_month_name"], data["lunar_day_name"]
    )
    draw_centered_text(draw, cx, cy, lunar_str, fill=1, font=font32, img_width=W, img_height=H)
    _, th = text_size(draw, lunar_str, font32)
    cy += th + 4

    ganzhi_str = "干支：{}年 {}月 {}日".format(
        data["year_ganzhi"], data["month_ganzhi"], data["day_ganzhi"]
    )
    parts = [ganzhi_str]
    if data["nayin_day"]:
        parts.append("纳音：{}".format(data["nayin_day"]))
    parts.append("生肖：{}".format(data["shengxiao"]))
    info_line = "\u3000".join(parts)
    draw_centered_text(draw, cx, cy, info_line, fill=1, font=font16, img_width=W, img_height=H)
    _, th = text_size(draw, info_line, font16)
    cy += th + 2

    extra_parts = []
    if data["jieqi"]:
        extra_parts.append("节气：{}".format(data["jieqi"]))
    all_festivals = data["festivals"] + data["other_festivals"]
    if all_festivals:
        extra_parts.append("节日：{}".format(" · ".join(all_festivals[:3])))
    if extra_parts:
        extra_str = "  |  ".join(extra_parts)
        draw_centered_text(draw, cx, cy, extra_str, fill=1, font=font16, img_width=W, img_height=H)
        _, th = text_size(draw, extra_str, font16)
        cy += th + 2

    cy += 4
    draw_h_line(draw, cy, margin, W - margin, fill=1, width=1)
    cy += 8

    row1_header_y = cy
    col_cx = [x1 + col_w // 2, x2 + col_w // 2, x3 + col_w // 2]
    draw_centered_text(draw, col_cx[0], row1_header_y, "宜", fill=1, font=font32, img_width=W, img_height=H)
    draw_centered_text(draw, col_cx[1], row1_header_y, "忌", fill=1, font=font32, img_width=W, img_height=H)
    draw_centered_text(draw, col_cx[2], row1_header_y, "吉神宜趋", fill=1, font=font32, img_width=W, img_height=H)
    _, hdr_th = text_size(draw, "宜", font32)

    row1_items_y = row1_header_y + hdr_th + 6
    _draw_column_items(draw, x1, row1_items_y, col_w, data["yi"], font16, W, H, max_items=5)
    _draw_column_items(draw, x2, row1_items_y, col_w, data["ji"], font16, W, H, max_items=5)
    _draw_column_items(draw, x3, row1_items_y, col_w, data["jishen"], font16, W, H, max_items=5)

    cy = row1_header_y + hdr_th + 6 + 5 * 21 + 4
    draw_h_line(draw, cy, margin, W - margin, fill=1, width=1)
    cy += 8

    row2_header_y = cy
    draw_centered_text(draw, col_cx[0], row2_header_y, "凶煞宜忌", fill=1, font=font32, img_width=W, img_height=H)
    draw_centered_text(draw, col_cx[1], row2_header_y, "冲煞", fill=1, font=font32, img_width=W, img_height=H)
    draw_centered_text(draw, col_cx[2], row2_header_y, "彭祖百忌", fill=1, font=font32, img_width=W, img_height=H)

    row2_items_y = row2_header_y + hdr_th + 6
    _draw_column_items(draw, x1, row2_items_y, col_w, data["xiongsha"], font16, W, H, max_items=5)

    chong_items = []
    if data["chong_desc"]:
        chong_items.append(data["chong_desc"])
    if data["sha"]:
        chong_items.append("煞{}".format(data["sha"]))
    _draw_column_items(draw, x2, row2_items_y, col_w, chong_items, font16, W, H, max_items=5)

    pengzu_items = []
    if data["pengzu_gan"]:
        pengzu_items.append(data["pengzu_gan"])
    if data["pengzu_zhi"]:
        pengzu_items.append(data["pengzu_zhi"])
    _draw_column_items(draw, x3, row2_items_y, col_w, pengzu_items, font16, W, H, max_items=5)

    cy = row2_header_y + hdr_th + 6 + 5 * 21 + 4
    draw_h_line(draw, cy, margin, W - margin, fill=1, width=1)
    cy += 8

    bottom_parts = []
    if data["zhixing"]:
        bottom_parts.append("值星：{}".format(data["zhixing"]))
    if data["xiu"]:
        xiu_info = "二十八宿：{}".format(data["xiu"])
        if data["xiu_luck"]:
            xiu_info += "（{}）".format(data["xiu_luck"])
        bottom_parts.append(xiu_info)
    if data["liuyao"]:
        bottom_parts.append("六曜：{}".format(data["liuyao"]))

    bottom_line1 = "  |  ".join(bottom_parts)
    if bottom_line1:
        draw_centered_text(draw, cx, cy, bottom_line1, fill=1, font=font16, img_width=W, img_height=H)
        _, th = text_size(draw, bottom_line1, font16)
        cy += th + 4

    pos_parts = []
    if data["pos_xi"]:
        pos_parts.append("喜神：{}".format(data["pos_xi"]))
    if data["pos_fu"]:
        pos_parts.append("福神：{}".format(data["pos_fu"]))
    if data["pos_cai"]:
        pos_parts.append("财神：{}".format(data["pos_cai"]))
    if data["day_lu"]:
        pos_parts.append("日禄：{}".format(data["day_lu"]))

    bottom_line2 = "  |  ".join(pos_parts)
    if bottom_line2:
        draw_centered_text(draw, cx, cy, bottom_line2, fill=1, font=font16, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)