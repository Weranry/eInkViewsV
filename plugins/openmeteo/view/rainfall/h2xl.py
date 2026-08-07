import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.weather_data import fetch_hourly_precipitation
from .utils import (
    load_font, text_size,
    draw_safe_text, draw_separator,
)


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    data = fetch_hourly_precipitation(lat, lon, tz)

    img, draw = create_canvas("h2xl", palette_type="bwr", cmode=cmode)
    W = img.width
    H = img.height

    times = data["times"]
    precip = data["precipitation"]

    title_font = load_font(32)
    body_font = load_font(16)

    title_text = "降雨量"
    draw_safe_text(draw, (20, 12), title_text, fill=2, font=title_font, img_width=W, img_height=H)

    sep_y = 52
    draw_separator(draw, sep_y, W)

    total_precip = sum(precip)
    max_precip = max(precip) if precip else 0.0

    summary_y = sep_y + 10
    summary_text = f"24h {total_precip:.1f}mm"
    summary_tw, summary_th = text_size(draw, summary_text, body_font)
    draw_safe_text(draw, (20, summary_y), summary_text, fill=1, font=body_font, img_width=W, img_height=H)

    if max_precip > 0:
        peak_text = f"峰值 {max_precip:.1f}mm"
        peak_tw, _ = text_size(draw, peak_text, body_font)
        draw_safe_text(draw, (20 + summary_tw + 24, summary_y), peak_text, fill=1, font=body_font, img_width=W, img_height=H)

    chart_left = 44
    chart_right = W - 20
    chart_top = summary_y + summary_th + 16
    chart_bottom = H - 40

    chart_width = chart_right - chart_left
    chart_height = chart_bottom - chart_top

    if chart_height < 20:
        chart_height = 20

    if max_precip <= 0:
        max_precip = 1.0

    n = len(precip)
    if n < 2:
        return finalize_image_common(img, rotate=rotate, invert=invert)

    points = []
    for i in range(n):
        x = chart_left + int(i * chart_width / (n - 1))
        ratio = precip[i] / max_precip
        if ratio > 1.0:
            ratio = 1.0
        y = chart_bottom - int(ratio * chart_height)
        points.append((x, y))

    fill_points = [(chart_left, chart_bottom)]
    fill_points.extend(points)
    fill_points.append((chart_right, chart_bottom))
    draw.polygon(fill_points, fill=1)

    step = 3
    label_font = load_font(16)
    for i in range(0, n, step):
        x = chart_left + int(i * chart_width / (n - 1))
        raw_time = times[i] if i < len(times) else ""
        hour_label = ""
        if "T" in raw_time:
            hour_label = raw_time.split("T")[1][:2]
        label_tw, label_th = text_size(draw, hour_label, label_font)
        label_x = x - label_tw // 2
        if label_x < chart_left:
            label_x = chart_left
        if label_x + label_tw > chart_right:
            label_x = chart_right - label_tw
        draw_safe_text(draw, (label_x, chart_bottom + 4), hour_label, fill=1, font=label_font, img_width=W, img_height=H)

    return finalize_image_common(img, rotate=rotate, invert=invert)