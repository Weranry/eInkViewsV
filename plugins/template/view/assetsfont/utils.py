import os
from plugins.template.lib.get_date import get_today_and_utc_date

FONT_PATHS = {
    'default': 'assets/fonts/font.ttf',
}

def get_calendar_data(tz=None):
    return get_today_and_utc_date(tz=tz)
