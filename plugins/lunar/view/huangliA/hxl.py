from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font as get_font_global
from .utils import FONT_PATHS, get_huangliA_data
from PIL import ImageDraw

def wrap_text(text, font, max_width, max_lines=2):
    lines = []
    if font.getlength(text) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        current_line = words[0]
        for word in words[1:]:
            if font.getlength(current_line + ' ' + word) <= max_width and len(lines) < max_lines:
                current_line += ' ' + word
            else:
                if len(lines) < max_lines:
                    lines.append(current_line)
                    current_line = word
                else:
                    break
        if len(lines) < max_lines:
            lines.append(current_line)
    return lines

def generate_image(rotate=0, invert=False, tz=None, cmode=None):
    img, draw = create_canvas('hxl', palette_type='bwr', cmode=cmode)
    font_large = get_font_global(14, font_path=FONT_PATHS['default'])
    font_small = get_font_global(12, font_path=FONT_PATHS['default'])  # 最小12

    lunar_date, ganzhi_date, solar_date, yiji = get_huangliA_data(tz=tz)

    lunar_text = f"农历{lunar_date['lunar_month']}{lunar_date['lunar_day']}"
    draw.text((5, 5), lunar_text, font=font_large, fill=1)

    ganzhi_text = f"{ganzhi_date['ganzhi_year']} {ganzhi_date['ganzhi_month']}{ganzhi_date['ganzhi_day']} [{ganzhi_date['shengxiao']}]"
    draw.text((5, 22), ganzhi_text, font=font_small, fill=1)

    solar_text = f"{solar_date['solar_year']}年{solar_date['solar_month']}月{solar_date['solar_day']}日 {solar_date['weekday']} {solar_date['xingzuo']}"
    draw.text((5, 36), solar_text, font=font_small, fill=1)

    draw.line((5, 50, 195, 50), fill=1)

    draw.text((5, 55), "宜", font=font_large, fill=1)
    yi_text = ' '.join(yiji['Yi'])
    yi_lines = wrap_text(yi_text, font_small, 180)
    for i, line in enumerate(yi_lines):
        draw.text((20, 55 + (i+1) * 16), line, font=font_small, fill=1)

    draw.text((5, 90), "忌", font=font_large, fill=1)
    ji_text = ' '.join(yiji['Ji'])
    ji_lines = wrap_text(ji_text, font_small, 180)
    for i, line in enumerate(ji_lines):
        draw.text((20, 90 + (i+1) * 16), line, font=font_small, fill=1)

    return finalize_image_common(img, rotate=rotate, invert=invert)
