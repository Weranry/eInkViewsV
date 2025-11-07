from plugins.template.lib.get_date import get_today_and_utc_date

def to_json(**kwargs):
    # 从请求参数获取 tz，默认为 None
    tz = kwargs.get('tz')
    result = get_today_and_utc_date(tz=tz)
    return result
