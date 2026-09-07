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
    
    canvas, draw = create_canvas('h2xl', 'bwr', cmode=cmode)
    
    font_large = get_font(80, get_root_font_path('font.ttf'))
    font_medium = get_font(32, get_root_font_path('font.ttf'))
    font_small = get_font(16, get_root_font_path('font.ttf'))
    
    # Top half: height ~120
    draw.text((16, 16), "海洋潮汐", font=font_medium, fill=text_color)
    
    current_wave_str = f"{tide_data['current_wave_height']:.1f}m"
    draw.text((16, 64), current_wave_str, font=font_large, fill=red_color)
    
    # Section 2: Max/Min wave height
    draw.text((200, 16), "今日极限", font=font_small, fill=text_color)
    draw.text((200, 48), f"最高: {tide_data['max_wave']:.1f}m", font=font_small, fill=red_color)
    draw.text((200, 80), f"最低: {tide_data['min_wave']:.1f}m", font=font_small, fill=text_color)
    
    # Section 3: Period/Direction & Update time
    draw.text((300, 16), "海况细节", font=font_small, fill=text_color)
    draw.text((300, 48), f"波周期: {tide_data['current_wave_period']}", font=font_small, fill=text_color)
    draw.text((300, 80), f"浪向: {tide_data['current_wave_direction']}", font=font_small, fill=text_color)
    draw.text((300, 112), f"更新: {tide_data['update_time']}", font=font_small, fill=text_color)
    
    # Horizontal divider
    draw.line((16, 140, 384, 140), fill=text_color, width=2)
    
    # Bottom half: height ~160
    draw.text((16, 156), "24小时浪高预测", font=font_small, fill=text_color)
    
    chart_x = 64
    chart_y = 196
    chart_w = 400 - 16 - chart_x
    chart_h = 300 - 16 - chart_y
    
    draw_tide_chart(draw, chart_x, chart_y, chart_w, chart_h, tide_data['forecast_24h'], tide_data['min_wave'], tide_data['max_wave'], font_small, red_color, text_color)
    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
