from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.moon_phase import draw_moon_sprite
from .utils import get_moon_data, load_font, wrap_by_space

W, H = 384, 184
MOON_SIZE = 110


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    now, moon, lat, lon = get_moon_data(tz, lat=kwargs.get('lat'), lon=kwargs.get('lon'))
    img, draw = create_canvas('hxl', 'bwr', cmode=cmode)

    # 月相图案（左侧）：轮廓与旋转都在精灵内部完成，这里只负责居中贴图
    cx, cy = 78, 92
    radius = MOON_SIZE // 2
    sprite = draw_moon_sprite(moon['phase_angle'], size=MOON_SIZE, rotation=moon['rotation'])
    img.paste(1, (cx - radius, cy - radius), mask=sprite.split()[3])

    # 相位名（右侧，最多两行）
    text_x = 148
    max_w = W - text_x - 12
    name_font = load_font(32)
    for i, line in enumerate(wrap_by_space(moon['phase_name'], name_font, max_w, max_lines=2)):
        draw.text((text_x, 10 + i * 32), line, fill=2, font=name_font)

    draw.line([(text_x, 78), (W - 12, 78)], fill=1, width=1)

    # 详细数据（右侧）
    info_font = load_font(16)
    nnm = moon['next_new_moon']
    nfm = moon['next_full_moon']
    draw.text((text_x, 84), f"Illum: {moon['illumination']:.1f}%", fill=1, font=info_font)
    draw.text((text_x, 102), f"Age: {moon['moon_age']:.1f}d", fill=1, font=info_font)
    draw.text((text_x, 120), f"New: {nnm.strftime('%m/%d %H:%M')}", fill=1, font=info_font)
    draw.text((text_x, 138), f"Full: {nfm.strftime('%m/%d %H:%M')}", fill=1, font=info_font)

    # 底部整行：经纬度 + 本地时间
    bottom = f"Lat {lat:.2f}  Lon {lon:.2f}   {now.strftime('%Y-%m-%d %H:%M')}"
    draw.text((12, H - 24), bottom, fill=1, font=info_font)

    return finalize_image_common(img, rotate=rotate, invert=invert)
