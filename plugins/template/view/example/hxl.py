from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font as get_font_global

def generate_image(rotate=0, invert=False, tz=None, cmode=None):
    img, draw = create_canvas('hxl', palette_type='bw', cmode=cmode)
    width, height = img.size
    # 计算每一部分的宽度
    part_width = width // 5
    # 画4条竖线（分成5部分）
    for i in range(1, 5):
        x = i * part_width
        draw.line([(x, 0), (x, height)], fill=1, width=1)
    # 可选：在每个区域写上编号
    font = get_font_global(24, font_path='assets/fonts/font.ttf')
    for i in range(5):
        text = str(i + 1)
        tx = i * part_width + part_width // 2 - 8
        ty = height // 2 - 12
        draw.text((tx, ty), text, font=font, fill=0)
    return finalize_image_common(img, rotate=rotate, invert=invert)
