from lunar_python import Solar
from datetime import datetime


def get_huangli_data():
    today = datetime.now()
    solar = Solar.fromYmd(today.year, today.month, today.day)
    lunar = solar.getLunar()

    jieqi = lunar.getJieQi()
    festivals = lunar.getFestivals() if lunar.getFestivals() else []
    other_festivals = lunar.getOtherFestivals() if lunar.getOtherFestivals() else []

    yi_list = list(lunar.getDayYi()) if lunar.getDayYi() else []
    ji_list = list(lunar.getDayJi()) if lunar.getDayJi() else []
    jishen_list = list(lunar.getDayJiShen()) if lunar.getDayJiShen() else []
    xiongsha_list = list(lunar.getDayXiongSha()) if lunar.getDayXiongSha() else []

    chong_desc = lunar.getDayChongDesc()
    chong_sx = lunar.getDayChongShengXiao()
    chong_gz = lunar.getDayChongGan()
    sha = lunar.getDaySha()
    zhixing = lunar.getZhiXing()

    pengzu_gan = lunar.getPengZuGan()
    pengzu_zhi = lunar.getPengZuZhi()

    nayin_year = lunar.getYearNaYin()
    nayin_month = lunar.getMonthNaYin()
    nayin_day = lunar.getDayNaYin()

    pos_xi = lunar.getPositionXiDesc()
    pos_fu = lunar.getPositionFuDesc()
    pos_cai = lunar.getPositionCaiDesc()

    xiu = lunar.getXiu()
    xiu_luck = lunar.getXiuLuck()

    liuyao = lunar.getLiuYao()

    day_lu = lunar.getDayLu()

    return {
        "solar_year": solar.getYear(),
        "solar_month": solar.getMonth(),
        "solar_day": solar.getDay(),
        "weekday": solar.getWeekInChinese(),

        "lunar_year": lunar.getYear(),
        "lunar_month": lunar.getMonth(),
        "lunar_day": lunar.getDay(),
        "lunar_month_name": lunar.getMonthInChinese(),
        "lunar_day_name": lunar.getDayInChinese(),

        "year_ganzhi": lunar.getYearInGanZhi(),
        "month_ganzhi": lunar.getMonthInGanZhi(),
        "day_ganzhi": lunar.getDayInGanZhi(),

        "shengxiao": lunar.getYearShengXiao(),

        "nayin_year": nayin_year if nayin_year else "",
        "nayin_month": nayin_month if nayin_month else "",
        "nayin_day": nayin_day if nayin_day else "",

        "jieqi": jieqi if jieqi else "",

        "festivals": festivals,
        "other_festivals": other_festivals,

        "yi": yi_list,
        "ji": ji_list,
        "jishen": jishen_list,
        "xiongsha": xiongsha_list,

        "chong_desc": chong_desc if chong_desc else "",
        "chong_sx": chong_sx if chong_sx else "",
        "chong_gz": chong_gz if chong_gz else "",
        "sha": sha if sha else "",

        "zhixing": zhixing if zhixing else "",

        "pengzu_gan": pengzu_gan if pengzu_gan else "",
        "pengzu_zhi": pengzu_zhi if pengzu_zhi else "",

        "pos_xi": pos_xi if pos_xi else "",
        "pos_fu": pos_fu if pos_fu else "",
        "pos_cai": pos_cai if pos_cai else "",

        "xiu": xiu if xiu else "",
        "xiu_luck": xiu_luck if xiu_luck else "",

        "liuyao": liuyao if liuyao else "",

        "day_lu": day_lu if day_lu else "",
    }