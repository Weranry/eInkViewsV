import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import importlib

canvas_factory = importlib.import_module("modules.generate_views.canvas_factory")
create_canvas = canvas_factory.create_canvas
finalize_image_common = canvas_factory.finalize_image_common

from ...lib.demo_data import build_demo_data
from .utils import load_font, draw_panel, text_size


def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    img, draw = create_canvas('hxl', palette_type='bwr', cmode=cmode)
    data = build_demo_data(
        a=kwargs.get('a'),
        b=kwargs.get('b'),
        tz=tz,
        title=kwargs.get('title'),
        subtitle=kwargs.get('subtitle'),
        left=kwargs.get('left'),
        right=kwargs.get('right'),
        note=kwargs.get('note'),
    )

    title_font = load_font(24)
    body_font = load_font(16)
    small_font = load_font(16)

    draw.text((16, 12), str(data['meta']['title']), fill=2, font=title_font)
    left_y = 56
    right_y = 56
    draw_panel(draw, 16, left_y, 160, 'Left', data['detail']['left'], body_font, body_font)
    draw_panel(draw, 200, right_y, 160, 'Right', data['detail']['right'], body_font, body_font)

    note = str(data['detail']['note'])
    note_w, note_h = text_size(draw, note, small_font)
    draw.text((img.width - 16 - note_w, img.height - 16 - note_h), note, fill=1, font=small_font)

    return finalize_image_common(img, rotate=rotate, invert=invert)
