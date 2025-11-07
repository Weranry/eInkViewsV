from ...lib.today_huangli import todayhuangli

FONT_PATHS = {
    'default': 'assets/fonts/font.ttf',
    # 可扩展更多字体类型
}

def get_huangli_data(tz=None):
    hl = todayhuangli(tz=tz)
    jishen = hl.get_jishen()
    taishen = hl.get_taishen()
    taisui = hl.get_taisui()
    pengzubaiji = hl.get_pengzubaiji()
    ershibaxingxiu = hl.get_ershibaxingxiu()
    chongsha = hl.get_chongsha()
    return jishen, taishen, taisui, pengzubaiji, ershibaxingxiu, chongsha
