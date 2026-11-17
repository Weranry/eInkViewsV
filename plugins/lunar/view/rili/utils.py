from ...lib.date_calculator import DateCalculator

FONT_PATHS = {
    'default': 'assets/fonts/font.ttf',
    # 可扩展更多字体类型
}

def get_calendar_data(tz=None):
    dc = DateCalculator(tz)
    solar = dc.get_solar_date()
    lunar = dc.get_lunar_date()
    ganzhi = dc.get_ganzhi_date()
    season = dc.get_season_info()
    festival = dc.get_festival_info()
    return solar, lunar, ganzhi, season, festival
