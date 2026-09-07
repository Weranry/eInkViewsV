from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from modules.errors.errors import ParamError
from plugins.openmeteo.lib.tide_fetcher import fetch_tide_data
from .utils import draw_tide_chart

def generate_image(rotate=0, invert=False, tz=None, cmode=None, lat=None, lon=None, **kwargs):
    if not lat or not lon:
        raise ParamError("Coordinates (lat, lon) are strictly required.")
        
    tide_data = fetch_tide_data(lat, lon, tz)
    
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    red_color = (255, 0, 0)
    
    canvas, draw = create_canvas('hxl', 'bwr', cmode=cmode)
    
    font_large = get_font(64, get_root_font_path('font.ttf'))
    font_medium = get_font(32, get_root_font_path('font.ttf'))
    font_small = get_font(16, get_root_font_path('font.ttf'))
    
    # Left column: width ~140
    # Title
    draw.text((16, 16), "海洋潮汐", font=font_medium, fill=text_color)
    
    # Current wave height
    current_wave_str = f"{tide_data['current_wave_height']:.1f}m"
    draw.text((16, 64), current_wave_str, font=font_large, fill=red_color)
    
    # Additional data
    wave_period_str = f"周期: {tide_data['current_wave_period']}"
    wave_dir_str = f"浪向: {tide_data['current_wave_direction']}"
    draw.text((16, 136), wave_period_str, font=font_small, fill=text_color)
    draw.text((16, 152), wave_dir_str, font=font_small, fill=text_color)
    
    # Divider
    draw.line((140, 16, 140, 168), fill=text_color, width=2)
    
    # Right column: width ~244
    draw.text((156, 16), "24H 浪高预测", font=font_small, fill=text_color)
    
    # Chart area
    chart_x = 196
    chart_y = 64
    chart_w = 384 - 16 - chart_x
    chart_h = 168 - 16 - 64
    
    draw_tide_chart(draw, chart_x, chart_y, chart_w, chart_h, tide_data['forecast_24h'], tide_data['min_wave'], tide_data['max_wave'], font_small, red_color, text_color)
    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
