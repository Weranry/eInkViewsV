from lunar_python import Solar, Lunar
from datetime import datetime
import calendar


def get_today_data():
    today = datetime.now()
    return get_date_data(today.year, today.month, today.day)


def get_date_data(year, month, day):
    solar = Solar.fromYmd(year, month, day)
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
        "lunar_month": lunar.getMonth(),
        "lunar_day": lunar.getDay(),
        "year_ganzhi": lunar.getYearInGanZhi(),
        "month_ganzhi": lunar.getMonthInGanZhi(),
        "day_ganzhi": lunar.getDayInGanZhi(),
        "shengxiao": lunar.getYearShengXiao(),
        "jieqi": jieqi if jieqi else None,
        "festivals": festivals if festivals else [],
        "other_festivals": other_festivals if other_festivals else [],
        "yi": yi_list[:6] if yi_list else [],
        "ji": ji_list[:6] if ji_list else [],
    }


def get_month_data(year, month):
    today = datetime.now()
    days = []

    total_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.weekday(year, month, 1)

    for day_idx in range(1, total_days + 1):
        solar = Solar.fromYmd(year, month, day_idx)
        lunar = solar.getLunar()

        weekday_num = calendar.weekday(year, month, day_idx)
        jieqi = lunar.getJieQi()
        festivals = lunar.getFestivals()
        other_festivals = lunar.getOtherFestivals()

        days.append({
            "solar_day": day_idx,
            "lunar_month": lunar.getMonth(),
            "lunar_day": lunar.getDay(),
            "lunar_month_name": lunar.getMonthInChinese(),
            "lunar_day_name": lunar.getDayInChinese(),
            "weekday": solar.getWeekInChinese(),
            "weekday_num": weekday_num,
            "is_today": (
                year == today.year
                and month == today.month
                and day_idx == today.day
            ),
            "is_weekend": weekday_num in (5, 6),
            "jieqi": jieqi if jieqi else None,
            "festivals": festivals if festivals else [],
            "other_festivals": other_festivals if other_festivals else [],
            "is_current_month": True,
        })

    return {
        "year": year,
        "month": month,
        "first_weekday_offset": (first_weekday + 1) % 7,
        "total_days": total_days,
        "days": days,
    }