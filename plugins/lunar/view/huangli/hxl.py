from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font as get_font_global
from .utils import FONT_PATHS, get_huangli_data
from PIL import ImageDraw

def generate_image(rotate=0, invert=False, tz=None, cmode=None):
    img, draw = create_canvas('hxl', palette_type='bwr', cmode=cmode)
    jishen, taishen, taisui, pengzubaiji, ershibaxingxiu, chongsha = get_huangli_data(tz=tz)

    title_font = get_font_global(16, font_path=FONT_PATHS['default'])
    font = get_font_global(10, font_path=FONT_PATHS['default'])
    draw.text((100, 14), "黄历", fill=1, font=title_font, anchor='mm')

    jishen_keys = list(jishen.keys())
    jishen_values = list(jishen.values())
    jishen_count = len(jishen_keys)
    start_x = 100 - (jishen_count - 1) * 30 // 2
    for i, (key, value) in enumerate(zip(jishen_keys, jishen_values)):
        x = start_x + i * 30
        draw.text((x, 28), key, fill=1, font=font, anchor='mm')
        draw.text((x, 42), value, fill=1, font=font, anchor='mm')

    draw.line([(15, 55), (185, 55)], fill=1, width=1)
    draw.line([(100, 55), (100, 105)], fill=1, width=1)

    left_x = 57
    draw.text((left_x, 65), "太岁", fill=1, font=font, anchor='mm')
    draw.text((left_x, 77), taisui, fill=1, font=font, anchor='mm')
    draw.text((left_x, 92), "胎神", fill=1, font=font, anchor='mm')
    draw.text((left_x, 105), taishen, fill=1, font=font, anchor='mm')

    right_x = 143
    draw.text((right_x, 65), "冲煞", fill=1, font=font, anchor='mm')
    draw.text((right_x, 77), chongsha, fill=1, font=font, anchor='mm')
    draw.text((right_x, 92), "二十八宿", fill=1, font=font, anchor='mm')
    draw.text((right_x, 105), ershibaxingxiu, fill=1, font=font, anchor='mm')

    draw.line([(15, 117), (185, 117)], fill=1, width=1)

    bz_font = get_font_global(12, font_path=FONT_PATHS['default'])
    draw.text((100, 125), "彭祖百忌", fill=1, font=bz_font, anchor='mm')
    draw.text((100, 140), pengzubaiji, fill=1, font=font, anchor='mm')
    return finalize_image_common(img, rotate=rotate, invert=invert)
