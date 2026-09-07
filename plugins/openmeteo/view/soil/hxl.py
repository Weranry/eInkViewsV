import os
from PIL import ImageDraw
from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from plugins.openmeteo.lib.soil_fetcher import fetch_soil_data

def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    lat = kwargs.get("lat")
    lon = kwargs.get("lon")
    data = fetch_soil_data(lat, lon, tz)
    canvas, draw = create_canvas("hxl", "bwr", cmode=cmode)

    f_title = get_font(32, get_root_font_path("font.ttf"))
    f_val = get_font(32, get_root_font_path("font.ttf"))
    f_unit = get_font(16, get_root_font_path("font.ttf"))

    draw.line((191, 0, 191, 184), fill=(0, 0, 0), width=2)
    draw.line((0, 91, 384, 91), fill=(0, 0, 0), width=2)
    
    centers = [(96, 46), (288, 46), (96, 138), (288, 138)]
    layers = data.get("layers", [])

    for i, (cx, cy) in enumerate(centers):
        if i >= len(layers): continue
        layer = layers[i]
        depth = layer.get("depth", "?")
        temp = layer.get("temperature")
        moist = layer.get("moisture")
        
        label = f"深度: {depth}"
        bb = draw.textbbox((0, 0), label, font=f_title)
        draw.text((cx - (bb[2]-bb[0])//2, cy - 40), label, fill=(0, 0, 0), font=f_title)

        t_str = f"{temp}" if temp is not None else "--"
        tcolor = (255, 0, 0) if temp is not None and (temp > 30 or temp < 5) else (0, 0, 0)
        
        bb_t = draw.textbbox((0,0), t_str + "\u00b0C", font=f_val)
        draw.text((cx - 86, cy), t_str + "\u00b0C", fill=tcolor, font=f_val)
        
        m_str = f"{moist}" if moist is not None else "--"
        mcolor = (255, 0, 0) if moist is not None and moist < 0.1 else (0, 0, 0) # e.g., low moisture red
        draw.text((cx + 10, cy), m_str + " %", fill=mcolor, font=f_val)
        
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
