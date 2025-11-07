from modules.common_timezone import now_in_timezone
import datetime

DEFAULT_DATE_FMT = '%Y-%m-%d %H:%M:%S'

def get_today_and_utc_date(tz=None):
    """
    返回两个字段：
    - date: 严格受tz参数控制（tz=None时为本地/默认时区，否则为指定时区）
    - utc_date: 始终为当前UTC时间（纯粹的UTC，不受tz影响）
    """
    # 第一条：正常受tz控制
    local_dt = now_in_timezone(tz)
    # 第二条：纯粹的UTC时间
    utc_dt = datetime.datetime.now(datetime.timezone.utc)
    return {
        "date": local_dt.strftime(DEFAULT_DATE_FMT),
        "utc_date": utc_dt.strftime(DEFAULT_DATE_FMT)
    }
