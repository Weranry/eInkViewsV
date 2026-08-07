import datetime
import os

try:
    from config import DEFAULT_TIMEZONE_OFFSET
except ImportError:
    DEFAULT_TIMEZONE_OFFSET = None


def _resolve_timezone(param_offset=None):
    if param_offset is not None:
        try:
            return float(param_offset)
        except (ValueError, TypeError):
            pass
        try:
            from zoneinfo import ZoneInfo
            return ZoneInfo(str(param_offset))
        except Exception:
            pass
    if DEFAULT_TIMEZONE_OFFSET is not None:
        return float(DEFAULT_TIMEZONE_OFFSET)
    return None


def get_timezone_offset(param_offset=None):
    tz = _resolve_timezone(param_offset)
    if tz is None:
        return None
    if isinstance(tz, datetime.tzinfo):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        return tz.utcoffset(utc_now).total_seconds() / 3600
    return tz


def now_in_timezone(param_offset=None):
    tz = _resolve_timezone(param_offset)
    if tz is None:
        return datetime.datetime.now()
    if isinstance(tz, datetime.tzinfo):
        return datetime.datetime.now(tz)
    utc_now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    return utc_now + datetime.timedelta(hours=tz)


def convert_utc_to_local(dt_utc, param_offset=None):
    tz = _resolve_timezone(param_offset)
    if tz is None:
        return dt_utc
    if isinstance(tz, datetime.tzinfo):
        if hasattr(dt_utc, 'tzinfo') and dt_utc.tzinfo is not None:
            dt_utc = dt_utc.astimezone(datetime.timezone.utc)
        else:
            dt_utc = dt_utc.replace(tzinfo=datetime.timezone.utc)
        return dt_utc.astimezone(tz).replace(tzinfo=None)
    if hasattr(dt_utc, 'tzinfo') and dt_utc.tzinfo is not None:
        dt_utc = dt_utc.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt_utc + datetime.timedelta(hours=tz)