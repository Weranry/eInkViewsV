from lunar_python import Solar, Lunar
from datetime import datetime


def get_calendar_data():
    today = datetime.now()
    solar = Solar.fromYmd(today.year, today.month, today.day)
    lunar = solar.getLunar()

    jieqi = lunar.getJieQi()
    festivals = lunar.getFestivals()
    other_festivals = lunar.getOtherFestivals()
    yi_list = lunar.getDayYi()
    ji_list = lunar.getDayJi()

    return {
        "solar_year": solar.getYear(),
        "solar_month": solar.getMonth(),
        "solar_day": solar.getDay(),
        "weekday": solar.getWeekInChinese(),
        "lunar_year": lunar.getYear(),
        "lunar_month_name": lunar.getMonthInChinese(),
        "lunar_day_name": lunar.getDayInChinese(),
        "year_ganzhi": lunar.getYearInGanZhi(),
        "month_ganzhi": lunar.getMonthInGanZhi(),
        "day_ganzhi": lunar.getDayInGanZhi(),
        "shengxiao": lunar.getYearShengXiao(),
        "jieqi": jieqi if jieqi else None,
        "festivals": festivals if festivals else [],
        "other_festivals": other_festivals if other_festivals else [],
        "yi": yi_list[:4] if yi_list else [],
        "ji": ji_list[:4] if ji_list else [],
    }