from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from ...lib.fetcher import ScheduleFetcher
from modules.errors.errors import ParamError
from .utils import render_schedule

def generate_image(rotate=0, invert=False, tz=None, cmode=None, json_name='course_schedule', **kwargs):
    try:
        fetcher = ScheduleFetcher(json_name=json_name)
        schedule_data = fetcher.fetch(tz=tz)
    except Exception as e:
        raise ParamError(f'Fetch failed: {str(e)}')

    size_key = kwargs.get('size', 'hxl')
    canvas, draw = create_canvas(size_key, 'bwr', cmode=cmode)

    render_schedule(canvas, draw, schedule_data)
    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
