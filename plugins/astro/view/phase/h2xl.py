from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.moon_phase import draw_moon_sprite
from .utils import get_moon_data, load_font, wrap_by_space

W, H = 400, 300
MOON_SIZE = 170


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    now, moon, lat, lon = get_moon_data(tz, lat=kwargs.get('lat'), lon=kwargs.get('lon'))
    img, draw = create_canvas('h2xl', 'bwr', cmode=cmode)

    # 月相图案（左侧）：轮廓与旋转都在精灵内部完成，这里只负责居中贴图
    cx, cy = 105, 150
    radius = MOON_SIZE // 2
    sprite = draw_moon_sprite(moon['phase_angle'], size=MOON_SIZE, rotation=moon['rotation'])
    img.paste(1, (cx - radius, cy - radius), mask=sprite.split()[3])

    # 相位名（右侧，最多两行）
    text_x = 210
    margin = 20
    max_w = W - text_x - margin
    name_font = load_font(32)
    for i, line in enumerate(wrap_by_space(moon['phase_name'], name_font, max_w, max_lines=2)):
        draw.text((text_x, 24 + i * 32), line, fill=2, font=name_font)

    draw.line([(text_x, 100), (W - margin, 100)], fill=1, width=1)

    # 详细数据（右侧）
    info_font = load_font(16)
    draw.text((text_x, 112), f"Illumination: {moon['illumination']:.1f}%", fill=1, font=info_font)
    draw.text((text_x, 134), f"Moon Age: {moon['moon_age']:.2f} days", fill=1, font=info_font)
    draw.text((text_x, 156), f"Phase Angle: {moon['phase_angle']:.1f}", fill=1, font=info_font)

    draw.line([(text_x, 182), (W - margin, 182)], fill=1, width=1)

    nnm = moon['next_new_moon']
    nfm = moon['next_full_moon']
    draw.text((text_x, 194), f"Next New:  {nnm.strftime('%m/%d %H:%M')}", fill=1, font=info_font)
    draw.text((text_x, 216), f"Next Full: {nfm.strftime('%m/%d %H:%M')}", fill=1, font=info_font)

    # 底部整行：经纬度 + 时区；下一行本地时间（月亮已结束，可横跨全宽）
    draw.text((20, 248), f"Lat {lat:.2f}  Lon {lon:.2f}   TZ {tz or 'UTC'}", fill=1, font=info_font)
    draw.text((20, 272), now.strftime('%Y-%m-%d %H:%M'), fill=1, font=info_font)

    return finalize_image_common(img, rotate=rotate, invert=invert)
