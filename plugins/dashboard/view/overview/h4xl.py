import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.calendar_data import get_calendar_data
from ...lib.weather_data import fetch_weather, wind_direction_text
from ...lib.news_data import fetch_news
from ...lib.hitokoto_data import fetch_hitokoto
from ...lib.history_data import fetch_history_today
from .utils import (
    load_font, load_icon_font, text_size,
    draw_safe_text, draw_h_line, draw_v_line,
    wrap_text, truncate_text,
)


def generate_image(rotate=0, invert=False, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    tz = kwargs.get("tz")

    cal_data = get_calendar_data()
    weather_data = fetch_weather(lat, lon, tz)
    news_items = fetch_news(max_items=10)
    hitokoto = fetch_hitokoto()
    history_items = fetch_history_today()

    img, draw = create_canvas("h4xl", palette_type="bw", cmode=cmode)
    W = img.width
    H = img.height

    margin = 8
    divider_x = 380
    left_x = margin
    left_w = divider_x - margin - 6
    right_x = divider_x + 6
    right_w = W - margin - right_x

    title_font = load_font(32)
    body_font = load_font(16)
    temp_font = load_font(48)
    icon_font = load_icon_font(48)
    small_icon_font = load_icon_font(16)

    _draw_left(
        draw, cal_data, weather_data,
        title_font, body_font, temp_font, icon_font, small_icon_font,
        left_x, left_w, W, H, margin, divider_x
    )
    _draw_right(
        draw, hitokoto, news_items, history_items,
        title_font, body_font,
        right_x, right_w, W, H, margin, divider_x
    )

    draw_v_line(draw, divider_x, margin, H - margin, fill=1, width=1)

    return finalize_image_common(img, rotate=rotate, invert=invert)


def _draw_left(draw, cal, wth, title_font, body_font, temp_font, icon_font, small_icon_font,
               left_x, left_w, W, H, margin, divider_x):
    cy = margin

    cy = _draw_date_section(draw, cal, title_font, body_font, left_x, left_w, W, H, cy)
    cy = _draw_weather_section(draw, wth, title_font, body_font, temp_font, icon_font,
                               left_x, left_w, W, H, cy, divider_x)
    _draw_forecast_section(draw, wth, body_font, small_icon_font,
                           left_x, left_w, W, H, cy, divider_x)


def _draw_date_section(draw, cal, title_font, body_font, left_x, left_w, W, H, cy):
    solar_str = "{}年{}月{}日".format(cal["solar_year"], cal["solar_month"], cal["solar_day"])
    draw_safe_text(draw, (left_x, cy), solar_str, fill=1, font=title_font, img_width=W, img_height=H)
    _, th = text_size(draw, solar_str, title_font)
    cy += th + 2

    weekday_str = "星期{}".format(cal["weekday"])
    draw_safe_text(draw, (left_x, cy), weekday_str, fill=1, font=title_font, img_width=W, img_height=H)
    _, th = text_size(draw, weekday_str, title_font)
    cy += th + 2

    lunar_str = "农历 {}年 {}月 {}".format(
        cal["year_ganzhi"], cal["lunar_month_name"], cal["lunar_day_name"]
    )
    draw_safe_text(draw, (left_x, cy), lunar_str, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, lunar_str, body_font)
    cy += th + 2

    ganzhi_str = "{}年  |  生肖: {}".format(cal["day_ganzhi"], cal["shengxiao"])
    draw_safe_text(draw, (left_x, cy), ganzhi_str, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, ganzhi_str, body_font)
    cy += th + 2

    festival_parts = cal["festivals"] + cal["other_festivals"]
    if cal["jieqi"]:
        jieqi_str = "节气: {}".format(cal["jieqi"])
        draw_safe_text(draw, (left_x, cy), jieqi_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, jieqi_str, body_font)
        cy += th + 2
    if festival_parts:
        fest_str = "节日: {}".format(" ".join(festival_parts[:3]))
        fest_str = truncate_text(draw, fest_str, body_font, left_w)
        draw_safe_text(draw, (left_x, cy), fest_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, fest_str, body_font)
        cy += th + 2

    if cal["yi"]:
        yi_str = "宜: {}".format(" ".join(cal["yi"]))
        yi_str = truncate_text(draw, yi_str, body_font, left_w)
        draw_safe_text(draw, (left_x, cy), yi_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, yi_str, body_font)
        cy += th + 2

    if cal["ji"]:
        ji_str = "忌: {}".format(" ".join(cal["ji"]))
        ji_str = truncate_text(draw, ji_str, body_font, left_w)
        draw_safe_text(draw, (left_x, cy), ji_str, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, ji_str, body_font)
        cy += th + 2

    return cy


def _draw_weather_section(draw, wth, title_font, body_font, temp_font, icon_font,
                          left_x, left_w, W, H, cy, divider_x):
    cy += 6
    draw_h_line(draw, cy, left_x, divider_x - 1, fill=1, width=1)
    cy += 8

    temp = wth["temperature"]
    feels = wth["feels_like"]
    humidity = wth["humidity"]
    wind_speed = wth["wind_speed"]
    wind_dir = wth["wind_direction"]
    pressure = wth["pressure"]
    weather_icon = wth["weather_icon"]
    weather_desc = wth["weather_desc"]

    icon_x = left_x
    icon_tw, icon_th = text_size(draw, weather_icon, icon_font)
    draw_safe_text(draw, (icon_x, cy), weather_icon, fill=1, font=icon_font, img_width=W, img_height=H)

    temp_str = "{:.0f}".format(temp) if temp is not None else "--"
    temp_text = "{}°C".format(temp_str)
    temp_tw, temp_th = text_size(draw, temp_text, temp_font)
    temp_x = icon_x + icon_tw + 10
    draw_safe_text(draw, (temp_x, cy), temp_text, fill=1, font=temp_font, img_width=W, img_height=H)

    icon_temp_h = max(icon_th, temp_th)
    cy += icon_temp_h + 4

    draw_safe_text(draw, (left_x, cy), weather_desc, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, weather_desc, body_font)
    cy += th + 2

    feels_str = "体感 {:.0f}°C".format(feels) if feels is not None else "体感 --"
    hum_str = "湿度 {:.0f}%".format(humidity) if humidity is not None else "湿度 --"
    detail_line1 = "{}  |  {}".format(feels_str, hum_str)
    draw_safe_text(draw, (left_x, cy), detail_line1, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, detail_line1, body_font)
    cy += th + 2

    wind_str = "风力 {:.1f} m/s".format(wind_speed) if wind_speed is not None else "风力 --"
    wind_dir_str = wind_direction_text(wind_dir)
    pres_str = "气压 {:.0f} hPa".format(pressure) if pressure is not None else "气压 --"
    detail_line2 = "{} {}  |  {}".format(wind_str, wind_dir_str, pres_str)
    detail_line2 = truncate_text(draw, detail_line2, body_font, left_w)
    draw_safe_text(draw, (left_x, cy), detail_line2, fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, detail_line2, body_font)
    cy += th + 2

    return cy


def _draw_forecast_section(draw, wth, body_font, small_icon_font,
                           left_x, left_w, W, H, cy, divider_x):
    cy += 6
    draw_h_line(draw, cy, left_x, divider_x - 1, fill=1, width=1)
    cy += 8

    draw_safe_text(draw, (left_x, cy), "未来三日", fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, "未来三日", body_font)
    cy += th + 4

    daily = wth.get("daily_forecast", [])
    day_labels = ["今日", "明天", "后天"]
    max_days = min(len(daily), 3)
    for i in range(max_days):
        if cy + 18 > H - 8:
            break
        d = daily[i]
        label = day_labels[i] if i < len(day_labels) else d["date"][-5:]

        icon_tw, _ = text_size(draw, d["weather_icon"], small_icon_font)
        draw_safe_text(draw, (left_x, cy), d["weather_icon"], fill=1,
                       font=small_icon_font, img_width=W, img_height=H)

        t_max = "{:.0f}".format(d["temp_max"]) if d["temp_max"] is not None else "--"
        t_min = "{:.0f}".format(d["temp_min"]) if d["temp_min"] is not None else "--"
        line = "{}  {}° / {}°  {}".format(label, t_max, t_min, d["weather_desc"])
        line = truncate_text(draw, line, body_font, left_w - icon_tw - 6)
        text_x = left_x + icon_tw + 6
        draw_safe_text(draw, (text_x, cy), line, fill=1, font=body_font, img_width=W, img_height=H)
        _, lh = text_size(draw, line, body_font)
        cy += max(lh, icon_tw) + 2


def _draw_right(draw, hitokoto, news_items, history_items, title_font, body_font,
                right_x, right_w, W, H, margin, divider_x):
    cy = margin

    cy = _draw_hitokoto_section(draw, hitokoto, body_font, right_x, right_w, W, H, cy)
    cy = _draw_news_section(draw, news_items, title_font, body_font,
                            right_x, right_w, W, H, cy, margin, divider_x)
    _draw_history_section(draw, history_items, body_font, right_x, right_w, W, H, cy, margin, divider_x)


def _draw_hitokoto_section(draw, hitokoto, body_font, right_x, right_w, W, H, cy):
    draw_safe_text(draw, (right_x, cy), "一言", fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, "一言", body_font)
    cy += th + 2

    quote_text = hitokoto["text"]
    if quote_text:
        quote_lines = wrap_text(draw, quote_text, body_font, right_w)
        for line in quote_lines[:2]:
            draw_safe_text(draw, (right_x, cy), line, fill=1, font=body_font, img_width=W, img_height=H)
            _, lh = text_size(draw, line, body_font)
            cy += lh + 1

    source_text = ""
    if hitokoto.get("author"):
        source_text = "—— {}".format(hitokoto["author"])
    elif hitokoto.get("source"):
        source_text = "—— {}".format(hitokoto["source"])
    if source_text:
        source_text = truncate_text(draw, source_text, body_font, right_w)
        draw_safe_text(draw, (right_x, cy), source_text, fill=1, font=body_font, img_width=W, img_height=H)
        _, th = text_size(draw, source_text, body_font)
        cy += th + 2

    return cy


def _draw_news_section(draw, news_items, title_font, body_font,
                       right_x, right_w, W, H, cy, margin, divider_x):
    cy += 6
    draw_h_line(draw, cy, divider_x + 1, W - margin, fill=1, width=1)
    cy += 8

    draw_safe_text(draw, (right_x, cy), "简讯", fill=1, font=title_font, img_width=W, img_height=H)
    _, th = text_size(draw, "简讯", title_font)
    cy += th + 4

    max_news = min(len(news_items), 8)
    for i in range(max_news):
        if cy + 18 > H - 8:
            break
        item = news_items[i]
        title = item["title"]
        source = item.get("source", "")
        if source:
            bullet = " {}  [{}]".format(title, source)
        else:
            bullet = " {}".format(title)
        bullet = truncate_text(draw, bullet, body_font, right_w)
        draw_safe_text(draw, (right_x, cy), bullet, fill=1, font=body_font, img_width=W, img_height=H)
        _, lh = text_size(draw, bullet, body_font)
        cy += lh + 2

    return cy


def _draw_history_section(draw, history_items, body_font, right_x, right_w, W, H, cy, margin, divider_x):
    cy += 6
    draw_h_line(draw, cy, divider_x + 1, W - margin, fill=1, width=1)
    cy += 8

    draw_safe_text(draw, (right_x, cy), "历史上的今天", fill=1, font=body_font, img_width=W, img_height=H)
    _, th = text_size(draw, "历史上的今天", body_font)
    cy += th + 4

    max_hist = min(len(history_items), 3)
    for i in range(max_hist):
        if cy + 18 > H - 8:
            break
        line = " {}".format(history_items[i])
        line = truncate_text(draw, line, body_font, right_w)
        draw_safe_text(draw, (right_x, cy), line, fill=1, font=body_font, img_width=W, img_height=H)
        _, lh = text_size(draw, line, body_font)
        cy += lh + 2