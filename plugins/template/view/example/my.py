from modules.generate_views.canvas_factory import create_custom_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font as get_font_global
from .utils import FONT_PATHS, get_calendar_data
from PIL import ImageDraw

def generate_image(rotate=0, invert=False, tz=None, cmode=None):
    img, draw = create_custom_canvas(200, 100, palette_type='bw', cmode=cmode)
    main_font = get_font_global(16, font_path=FONT_PATHS['default'])
    
    date_info = get_calendar_data(tz=tz)
    date_str = date_info["date"]
    utc_date_str = date_info["utc_date"]
    draw.text((0, 0), date_str, font=main_font, fill=1)
    draw.text((0, 30), utc_date_str, font=main_font, fill=1)
    return finalize_image_common(img, rotate=rotate, invert=invert)
