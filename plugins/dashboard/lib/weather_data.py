import requests
from modules.errors.errors import ParamError

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WMO_DESC_MAP = {
    0: '晴',
    1: '少云',
    2: '多云',
    3: '阴',
    45: '薄雾',
    48: '雾',
    51: '毛毛雨/细雨',
    53: '毛毛雨/细雨',
    55: '毛毛雨/细雨',
    61: '小雨',
    63: '中雨',
    65: '大雨',
    71: '小雪',
    73: '中雪',
    75: '大雪',
    77: '雪',
    80: '阵雨',
    81: '强阵雨',
    82: '强阵雨',
    85: '阵雪',
    86: '阵雪',
    95: '雷阵雨',
    96: '雷阵雨伴有冰雹',
    99: '雷阵雨伴有冰雹',
}

ICON_MAP = {
    '晴': '\uf1a1',
    '多云': '\uf1a2',
    '少云': '\uf1a3',
    '阴': '\uf1a5',
    '阵雨': '\uf1aa',
    '强阵雨': '\uf1ab',
    '雷阵雨': '\uf1ac',
    '雷阵雨伴有冰雹': '\uf1ae',
    '小雨': '\uf1af',
    '中雨': '\uf1b0',
    '大雨': '\uf1b1',
    '毛毛雨/细雨': '\uf1b3',
    '小雪': '\uf1c0',
    '中雪': '\uf1c1',
    '大雪': '\uf1c2',
    '雪': '\uf1cd',
    '薄雾': '\uf1ce',
    '雾': '\uf1cf',
}


def get_weather_icon(code):
    desc = WMO_DESC_MAP.get(code, "未知")
    icon = ICON_MAP.get(desc, "\uf1de")
    return icon, desc


def fetch_weather(lat, lon, tz):
    if lat is None or lon is None or tz is None:
        raise ParamError("仪表盘插件需要 lat、lon、tz 三个参数")

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (TypeError, ValueError):
        raise ParamError("lat、lon 必须为有效数值")

    params = {
        "latitude": lat_f,
        "longitude": lon_f,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "weather_code,wind_speed_10m,wind_direction_10m,"
            "surface_pressure,is_day"
        ),
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": str(tz),
        "forecast_days": 3,
    }

    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        raise ParamError("Open-Meteo API 请求超时")
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API 请求失败: {str(e)}")

    current = data.get("current", {})
    if not current:
        raise ParamError("Open-Meteo 未返回当前天气数据")

    weather_code = current.get("weather_code")
    icon, desc = get_weather_icon(weather_code)

    daily_data = data.get("daily", {})
    daily_forecast = _parse_daily(daily_data)

    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "weather_code": weather_code,
        "weather_icon": icon,
        "weather_desc": desc,
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "pressure": current.get("surface_pressure"),
        "is_day": current.get("is_day", 1),
        "time": current.get("time", ""),
        "daily_forecast": daily_forecast,
    }


def _parse_daily(daily):
    if not daily:
        return []
    times = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])

    result = []
    n = min(len(times), len(max_temps), len(min_temps), len(codes))
    for i in range(n):
        icon, desc = get_weather_icon(codes[i])
        result.append({
            "date": times[i],
            "temp_max": max_temps[i],
            "temp_min": min_temps[i],
            "weather_code": codes[i],
            "weather_icon": icon,
            "weather_desc": desc,
        })
    return result


def wind_direction_text(degrees):
    if degrees is None:
        return "--"
    directions = [
        "北", "东北偏北", "东北", "东北偏东",
        "东", "东南偏东", "东南", "东南偏南",
        "南", "西南偏南", "西南", "西南偏西",
        "西", "西北偏西", "西北", "西北偏北",
    ]
    idx = int((degrees + 11.25) / 22.5) % 16
    return directions[idx]