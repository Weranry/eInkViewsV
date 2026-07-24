import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib
from datetime import datetime

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.news_data import fetch_news
from .utils import (
    load_font, text_size, draw_safe_text,
    draw_h_line, draw_v_line, draw_text_block,
)


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    news_items = fetch_news(max_items=12)

    if len(news_items) < 5:
        raise ValueError("新闻条数不足，至少需要5条新闻")

    img, draw = create_canvas("h4xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    margin = 16
    col_gap = 16

    masthead_font = load_font(32)
    date_font = load_font(16)
    headline_font = load_font(48)
    subhead_font = load_font(32)
    summary_font = load_font(16)
    ticker_font = load_font(16)

    today_str = datetime.now().strftime("%Y年%m月%d日")

    masthead_text = "今日新闻"
    m_tw, m_th = text_size(draw, masthead_text, masthead_font)
    draw_safe_text(draw, (margin, 8), masthead_text, fill=1, font=masthead_font, img_width=W, img_height=H)

    date_tw, date_th = text_size(draw, today_str, date_font)
    draw_safe_text(draw, (W - margin - date_tw, 8 + (m_th - date_th) // 2), today_str, fill=1, font=date_font, img_width=W, img_height=H)

    header_bottom = 8 + m_th + 4
    draw_h_line(draw, header_bottom, margin, W - margin, fill=1, width=2)

    main_headline = news_items[0]
    headline_y = header_bottom + 8

    hl_title = main_headline["title"]
    hl_tw, hl_th = text_size(draw, hl_title, headline_font)
    if hl_tw > W - margin * 2:
        available_w = W - margin * 2
        draw_safe_text(draw, (margin, headline_y), hl_title, fill=2, font=headline_font, img_width=W, img_height=H)
    else:
        draw_safe_text(draw, (margin, headline_y), hl_title, fill=2, font=headline_font, img_width=W, img_height=H)

    headline_bottom = headline_y + hl_th + 6

    hl_summary = main_headline["summary"]
    if hl_summary:
        _, summary_th = text_size(draw, "Ag", summary_font)
        end_y, _ = draw_text_block(
            draw, (margin, headline_bottom), hl_summary,
            fill=1, font=summary_font, max_width=W - margin * 2, max_lines=2,
            img_width=W, img_height=H, line_spacing=4
        )
        headline_bottom = end_y + summary_th + 4

    draw_h_line(draw, headline_bottom + 4, margin, W - margin, fill=1, width=1)

    sub_start_y = headline_bottom + 14
    col_w = (W - margin * 2 - col_gap) // 2

    sub_news = news_items[1:5]

    positions = [
        (margin, sub_start_y),
        (margin + col_w + col_gap, sub_start_y),
        (margin, sub_start_y + 126),
        (margin + col_w + col_gap, sub_start_y + 126),
    ]

    _, sub_th = text_size(draw, "Ag", subhead_font)
    _, sum_th = text_size(draw, "Ag", summary_font)
    single_block_h = sub_th + 6 + sum_th * 2 + 16

    for i, item in enumerate(sub_news):
        if i >= len(positions):
            break
        col_x, col_y = positions[i]

        sub_title = item["title"]
        if len(sub_title) > 22:
            sub_title = sub_title[:22] + "..."

        sub_tw, sub_title_h = text_size(draw, sub_title, subhead_font)
        if sub_tw > col_w:
            draw_safe_text(draw, (col_x, col_y), sub_title, fill=1, font=subhead_font, img_width=W, img_height=H)
        else:
            draw_safe_text(draw, (col_x, col_y), sub_title, fill=1, font=subhead_font, img_width=W, img_height=H)

        summary_y = col_y + sub_title_h + 6
        sub_summary = item["summary"]
        if sub_summary:
            draw_text_block(
                draw, (col_x, summary_y), sub_summary,
                fill=1, font=summary_font, max_width=col_w, max_lines=2,
                img_width=W, img_height=H, line_spacing=4
            )

        if i % 2 == 0 and i < len(sub_news) - 1:
            draw_v_line(draw, margin + col_w + col_gap // 2, col_y, col_y + single_block_h, fill=1, width=1)

    ticker_y = H - 40
    draw_h_line(draw, ticker_y - 4, margin, W - margin, fill=1, width=1)

    ticker_items = news_items[5:11]
    if ticker_items:
        ticker_parts = []
        for item in ticker_items:
            short_title = item["title"]
            if len(short_title) > 18:
                short_title = short_title[:18] + ".."
            ticker_parts.append(short_title)

        ticker_text = "  ◆  ".join(ticker_parts)
        ticker_tw, ticker_th = text_size(draw, ticker_text, ticker_font)

        if ticker_tw > W - margin * 2:
            max_chars = 0
            test = ""
            for part in ticker_parts:
                candidate = test + "  ◆  " + part if test else part
                tw, _ = text_size(draw, candidate, ticker_font)
                if tw > W - margin * 2:
                    break
                test = candidate
                max_chars += 1
            ticker_text = test

        draw_safe_text(draw, (margin, ticker_y), ticker_text, fill=1, font=ticker_font, img_width=W, img_height=H)

        source_text = ""
        if news_items:
            source_text = f"来源: {news_items[0].get('source', '')}"
        if source_text:
            src_tw, _ = text_size(draw, source_text, ticker_font)
            draw_safe_text(draw, (W - margin - src_tw, ticker_y + ticker_th + 4), source_text, fill=1, font=ticker_font, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)