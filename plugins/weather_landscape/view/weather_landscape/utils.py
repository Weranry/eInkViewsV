from modules.generate_views.canvas_factory import (
    create_canvas,
    finalize_image_common,
)

def prepare_canvas(kind, palette_type='bwr', cmode=None):
    img, draw = create_canvas(kind, palette_type, cmode=cmode)
    return img, draw

def finalize_image(img, rotate=0, invert=False):
    return finalize_image_common(img, rotate=rotate, invert=invert)
