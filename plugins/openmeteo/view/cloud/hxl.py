import os
from PIL import ImageDraw
from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from plugins.openmeteo.lib.cloud_fetcher import fetch_cloud_data

def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    data = fetch_cloud_data(lat, lon, tz)
    canvas, draw = create_canvas("hxl", "bwr", cmode=cmode)

    f_title = get_font(32, get_root_font_path("font.ttf"))
    f_val = get_font(48, get_root_font_path("font.ttf"))
    f_unit = get_font(16, get_root_font_path("font.ttf"))

    draw.line((191, 0, 191, 184), fill=(0, 0, 0), width=2)
    draw.line((0, 91, 384, 91), fill=(0, 0, 0), width=2)
    
    layer_map = {"Total": "总云量", "High": "高空云", "Mid": "中层云", "Low": "低层云"}
    centers = [(96, 46), (288, 46), (96, 138), (288, 138)]
    layers = data.get("layers", [])

    for i, (cx, cy) in enumerate(centers):
        if i >= len(layers): continue
        layer = layers[i]
        raw_key = layer.get("layer", "?")
        label = layer_map.get(raw_key, raw_key)
        cover = layer.get("cover")
        
        # Title
        bb = draw.textbbox((0, 0), label, font=f_title)
        draw.text((cx - (bb[2]-bb[0])//2, cy - 38), label, fill=(0, 0, 0), font=f_title)

        # Value
        v_str = f"{cover}" if cover is not None else "--"
        vcolor = (255, 0, 0) if cover is not None and cover > 50 else (0, 0, 0)
        
        bb_v = draw.textbbox((0, 0), v_str, font=f_val)
        bb_u = draw.textbbox((0, 0), "%", font=f_unit)
        total_w = (bb_v[2]-bb_v[0]) + (bb_u[2]-bb_u[0])
        
        start_x = cx - total_w//2
        draw.text((start_x, cy - 4), v_str, fill=vcolor, font=f_val)
        draw.text((start_x + (bb_v[2]-bb_v[0]), cy + 22), "%", fill=vcolor, font=f_unit)
        
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
