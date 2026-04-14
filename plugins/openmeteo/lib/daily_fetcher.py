import requests
from modules.errors.errors import ParamError
from datetime import datetime

def fetch_daily_weather(lat, lon, tz='Asia/Shanghai'):
    if not lat or not lon:
        raise ParamError("lat and lon are required")
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": tz,
        "forecast_days": 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily = data.get('daily', {})
        times = daily.get('time', [])
        codes = daily.get('weather_code', [])
        t_max = daily.get('temperature_2m_max', [])
        t_min = daily.get('temperature_2m_min', [])
        
        days = []
        for i in range(min(5, len(times))):
            date_str = times[i]
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
            
            days.append({
                'date': date_str[-5:],  # "MM-DD"
                'weekday': weekday,
                'code': codes[i] if i < len(codes) else 0,
                't_max': round(t_max[i]) if i < len(t_max) and t_max[i] is not None else 0,
                't_min': round(t_min[i]) if i < len(t_min) and t_min[i] is not None else 0
            })
            
        return days
        
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API fetch failed: {str(e)}")
