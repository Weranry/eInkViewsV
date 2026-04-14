import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from plugins.openmeteo.lib.now_fetcher import fetch_now_weather
from modules.common_timezone import now_in_timezone

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, **kwargs):
    if not lat or not lon:
        lat = "52.52"  # fallback
        lon = "13.41"
    if not tz:
        tz = 'Asia/Shanghai'
        
    data = fetch_now_weather(lat, lon, tz)
    tz_str = 'None' # just string holder
    now_str = now_in_timezone(tz).strftime('%H:%M')
    
    canvas, draw = create_canvas('hxl', 'bwr', cmode=cmode) # 384x184
    
    # 1. title/time
    from modules.generate_views.font_loader import get_font, get_root_font_path
    font16 = get_font(16, get_root_font_path('font.ttf'))
    font32 = get_font(32, get_root_font_path('font.ttf'))
    font96 = get_font(96, get_root_font_path('font.ttf'))
    font_icon_112 = get_font(112, get_root_font_path('weather-icon.ttf'))
    
    code = data.get('weather_code', 0)
    from plugins.openmeteo.view.now.utils import get_weather_info, get_wind_dir
    desc, icon_char = get_weather_info(code)
    
    temp = round(data.get('temperature_2m', 0))
    temp_str = str(temp)
    temp_bbox = draw.textbbox((0,0), temp_str, font=font96)
    temp_w = temp_bbox[2] - temp_bbox[0]
    
    deg_str = "°C"
    deg_bbox = draw.textbbox((0,0), deg_str, font=font32)
    deg_w = deg_bbox[2] - deg_bbox[0]
    
    icon_bbox = draw.textbbox((0,0), icon_char, font=font_icon_112)
    icon_w = icon_bbox[2] - icon_bbox[0]
    icon_h = icon_bbox[3] - icon_bbox[1]
    
    desc_bbox = draw.textbbox((0,0), desc, font=font32)
    desc_w = desc_bbox[2] - desc_bbox[0]
    
    # 1. Top Bar
    py = 12
    time_w = draw.textbbox((0,0), now_str, font=font16)[2] - draw.textbbox((0,0), now_str, font=font16)[0]
    draw.text((384 - 16 - time_w, py), now_str, font=font16, fill=(0,0,0))
    
    # 2. Left Column (Temp & Desc)
    temp_y = py + 36
    draw.text((16, temp_y - 12), temp_str, font=font96, fill=(0,0,0))
    draw.text((16 + temp_w + 4, temp_y + 8), deg_str, font=font32, fill=(0,0,0))
    
    desc_y = 140
    draw.text((16, desc_y), desc, font=font32, fill=(255,0,0))
    
    # 3. Right Column (Icon)
    icon_x = 384 - 16 - icon_w
    icon_y = py + 28 + (184 - (py + 28) - icon_h) // 2
    if icon_y < py + 28: icon_y = py + 28
    draw.text((icon_x, icon_y), icon_char, font=font_icon_112, fill=(0,0,0))
    
    # 4. Middle Column (Details)
    mid_x = 16 + temp_w + deg_w + 24
    if mid_x < 160: mid_x = 160
    
    app_t = round(data.get('apparent_temperature', 0))
    humid = round(data.get('relative_humidity_2m', 0))
    wind_d = get_wind_dir(data.get('wind_direction_10m'))
    wind_s = round(data.get('wind_speed_10m', 0), 1)
    
    details = [
        f"体感 {app_t}°C",
        f"湿度 {humid}%",
        f"{wind_d}",
        f"{wind_s} km/h"
    ]
    
    mid_y = py + 44
    for i, d in enumerate(details):
        draw.text((mid_x, mid_y + i * 24), d, font=font16, fill=(0,0,0))
        
    draw.line([(mid_x - 8, mid_y), (mid_x - 8, mid_y + 4*24 - 6)], fill=(0,0,0), width=1)
    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)