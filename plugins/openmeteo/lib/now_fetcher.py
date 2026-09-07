import requests
from modules.errors.errors import ParamError

def fetch_now_weather(lat, lon, tz='Asia/Shanghai'):
    if not lat or not lon:
        raise ParamError("lat and lon are required")
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure",
        "timezone": tz
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['current']
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API fetch failed: {str(e)}")