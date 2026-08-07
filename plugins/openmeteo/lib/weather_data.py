import requests
from modules.errors.errors import ParamError

OPEN_METEO_CURRENT_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_weather(lat, lon, tz):
    if lat is None or lon is None or tz is None:
        raise ParamError("天气插件需要 lat、lon、tz 三个参数")

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
        "timezone": str(tz),
        "forecast_days": 1,
    }

    try:
        resp = requests.get(OPEN_METEO_CURRENT_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        raise ParamError("Open-Meteo API 请求超时")
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API 请求失败: {str(e)}")

    current = data.get("current", {})
    if not current:
        raise ParamError("Open-Meteo 未返回当前天气数据")

    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "weather_code": current.get("weather_code"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m"),
        "pressure": current.get("surface_pressure"),
        "is_day": current.get("is_day", 1),
        "time": current.get("time", ""),
        "lat": lat_f,
        "lon": lon_f,
        "tz": str(tz),
    }


def fetch_daily_forecast(lat, lon, tz, days=7):
    if lat is None or lon is None or tz is None:
        raise ParamError("天气插件需要 lat、lon、tz 三个参数")

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (TypeError, ValueError):
        raise ParamError("lat、lon 必须为有效数值")

    params = {
        "latitude": lat_f,
        "longitude": lon_f,
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "weather_code,precipitation_probability_max"
        ),
        "timezone": str(tz),
        "forecast_days": days,
    }

    try:
        resp = requests.get(OPEN_METEO_CURRENT_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        raise ParamError("Open-Meteo API 请求超时")
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API 请求失败: {str(e)}")

    daily = data.get("daily", {})
    if not daily:
        raise ParamError("Open-Meteo 未返回预报数据")

    days_data = []
    times = daily.get("time", [])
    temps_max = daily.get("temperature_2m_max", [])
    temps_min = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])
    precips = daily.get("precipitation_probability_max", [])

    for i in range(len(times)):
        days_data.append({
            "date": times[i] if i < len(times) else "",
            "temp_max": temps_max[i] if i < len(temps_max) else None,
            "temp_min": temps_min[i] if i < len(temps_min) else None,
            "weather_code": codes[i] if i < len(codes) else None,
            "precip_prob": precips[i] if i < len(precips) else None,
        })

    return days_data


def fetch_hourly_precipitation(lat, lon, tz):
    if lat is None or lon is None or tz is None:
        raise ParamError("天气插件需要 lat、lon、tz 三个参数")

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (TypeError, ValueError):
        raise ParamError("lat、lon 必须为有效数值")

    params = {
        "latitude": lat_f,
        "longitude": lon_f,
        "hourly": "precipitation,precipitation_probability",
        "timezone": str(tz),
        "forecast_days": 1,
    }

    try:
        resp = requests.get(OPEN_METEO_CURRENT_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        raise ParamError("Open-Meteo API 请求超时")
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API 请求失败: {str(e)}")

    hourly = data.get("hourly", {})
    if not hourly:
        raise ParamError("Open-Meteo 未返回小时级降水数据")

    times = hourly.get("time", [])
    precip = hourly.get("precipitation", [])
    precip_prob = hourly.get("precipitation_probability", [])

    if not times or not precip:
        raise ParamError("Open-Meteo 小时级降水数据不完整")

    return {
        "times": times,
        "precipitation": [p if p is not None else 0.0 for p in precip],
        "precipitation_probability": [p if p is not None else 0 for p in precip_prob],
    }