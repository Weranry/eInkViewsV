import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from plugins.openmeteo.lib.now_fetcher import fetch_now_weather
from plugins.openmeteo.view.now.utils import get_weather_info, get_wind_dir
from modules.common_timezone import now_in_timezone

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, **kwargs):
    if not lat or not lon:
        lat = "52.52"  # fallback
        lon = "13.41"
    if not tz:
        tz = 'Asia/Shanghai'
        
    data = fetch_now_weather(lat, lon, tz)
    
    now_str = now_in_timezone(tz).strftime('%H:%M')
    
    canvas, draw = create_canvas('h2xl', 'bwr', cmode=cmode) # 400x300
    
    from modules.generate_views.font_loader import get_font, get_root_font_path
    font16 = get_font(16, get_root_font_path('font.ttf'))
    font32 = get_font(32, get_root_font_path('font.ttf'))
    font48 = get_font(48, get_root_font_path('font.ttf'))
    font112 = get_font(112, get_root_font_path('font.ttf'))
    font_icon_144 = get_font(144, get_root_font_path('weather-icon.ttf'))
    
    code = data.get('weather_code', 0)
    desc, icon_char = get_weather_info(code)
    
    temp = round(data.get('temperature_2m', 0))
    temp_str = str(temp)
    temp_bbox = draw.textbbox((0,0), temp_str, font=font112)
    temp_w = temp_bbox[2] - temp_bbox[0]
    
    deg_str = "°C"
    deg_bbox = draw.textbbox((0,0), deg_str, font=font32)
    deg_w = deg_bbox[2] - deg_bbox[0]
    
    icon_bbox = draw.textbbox((0,0), icon_char, font=font_icon_144)
    icon_w = icon_bbox[2] - icon_bbox[0]
    
    desc_bbox = draw.textbbox((0,0), desc, font=font32)
    desc_w = desc_bbox[2] - desc_bbox[0]
    
    # 1. Top Bar
    py = 16
    time_w = draw.textbbox((0,0), now_str, font=font16)[2] - draw.textbbox((0,0), now_str, font=font16)[0]
    draw.text((400 - 16 - time_w, py), now_str, font=font16, fill=(0,0,0))
    
    # 2. Main Content (Icon and Temp)
    # Icon left
    draw.text((32, 60), icon_char, font=font_icon_144, fill=(0,0,0))
    
    # Temp right (aligned to edge)
    temp_x = 400 - 16 - temp_w - deg_w
    draw.text((temp_x, 60), temp_str, font=font112, fill=(0,0,0))
    draw.text((temp_x + temp_w + 4, 76), deg_str, font=font32, fill=(0,0,0))
    
    # Desc under Temp on right side
    desc_x = temp_x + (temp_w + deg_w - desc_w) // 2
    draw.text((desc_x, 160), desc, font=font32, fill=(255,0,0))
    
    # Apparent temp under Desc
    app_t = round(data.get('apparent_temperature', 0))
    app_str = f"体感温度 {app_t}°C"
    app_bbox = draw.textbbox((0,0), app_str, font=font16)
    app_w = app_bbox[2] - app_bbox[0]
    
    app_x = temp_x + (temp_w + deg_w - app_w) // 2
    draw.text((app_x, 210), app_str, font=font16, fill=(0,0,0))
    
    # 3. Bottom Columns (Humidity, Wind, Press)
    draw.line([(16, 246), (400 - 16, 246)], fill=(0,0,0), width=1)
    
    humid = round(data.get('relative_humidity_2m', 0))
    pressure = round(data.get('surface_pressure', 0))
    wind_d = get_wind_dir(data.get('wind_direction_10m'))
    wind_s = round(data.get('wind_speed_10m', 0), 1)
    
    cols = [
        ("相对湿度", f"{humid}%"),
        ("风向风速", f"{wind_d} {wind_s}"),
        ("地表气压", f"{pressure} hPa")
    ]
    
    col_w = (400 - 32) // 3
    for i, (lbl, val) in enumerate(cols):
        cx = 16 + i * col_w
        lbl_w = draw.textbbox((0,0), lbl, font=font16)[2] - draw.textbbox((0,0), lbl, font=font16)[0]
        val_w = draw.textbbox((0,0), val, font=font16)[2] - draw.textbbox((0,0), val, font=font16)[0]
        
        draw.text((cx + (col_w - lbl_w)//2, 254), lbl, font=font16, fill=(0,0,0))
        draw.text((cx + (col_w - val_w)//2, 276), val, font=font16, fill=(0,0,0))
        
        if i < 2:
            draw.line([(cx + col_w, 254), (cx + col_w, 296)], fill=(0,0,0), width=1)
            
    return finalize_image_common(canvas, rotate=rotate, invert=invert)