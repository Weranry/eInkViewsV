FONT_PATHS = {
    'default': 'assets/fonts/font.ttf',
    # 可扩展更多字体类型
}

from plugins.lunar.lib.today_huangli_A import todayhuangliA

def get_huangliA_data(tz=None):
    today = todayhuangliA(tz=tz)
    lunar_date = today.get_lunar_date()
    ganzhi_date = today.get_ganzhi_date()
    solar_date = today.get_solar_date()
    yiji = today.get_Day_Yiji()
    return lunar_date, ganzhi_date, solar_date, yiji
