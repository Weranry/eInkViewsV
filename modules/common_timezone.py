import datetime
import os

try:
    from config import DEFAULT_TIMEZONE_OFFSET
except ImportError:
    DEFAULT_TIMEZONE_OFFSET = None

def get_timezone_offset(param_offset=None):
    if param_offset is not None:
        try:
            return float(param_offset)
        except Exception:
            pass
    if DEFAULT_TIMEZONE_OFFSET is not None:
        return float(DEFAULT_TIMEZONE_OFFSET)
    return None  # 没有设置

def now_in_timezone(param_offset=None):
    offset = get_timezone_offset(param_offset)
    if offset is None:
        return datetime.datetime.now()  # 本机时间
    utc_now = datetime.datetime.utcnow()
    local_now = utc_now + datetime.timedelta(hours=offset)
    return local_now

def convert_utc_to_local(dt_utc, param_offset=None):
    offset = get_timezone_offset(param_offset)
    if offset is None:
        return dt_utc  # 不偏移
    if hasattr(dt_utc, 'tzinfo') and dt_utc.tzinfo is not None:
        dt_utc = dt_utc.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt_utc + datetime.timedelta(hours=offset)
