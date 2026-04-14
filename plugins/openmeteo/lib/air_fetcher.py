import requests
from modules.errors.errors import ParamError
from modules.common_timezone import now_in_timezone

def fetch_air_quality(lat, lon, tz='Asia/Shanghai'):
    if not lat or not lon:
        raise ParamError("lat and lon are required")
    
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,carbon_dioxide,nitrogen_dioxide,sulphur_dioxide,ozone,methane",
        "timezone": tz,
        "forecast_days": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ParamError(f"Open-Meteo API fetch failed: {str(e)}")
        
    try:
        hourly = data['hourly']
        hourly_units = data.get('hourly_units', {})
        current_time_str = now_in_timezone(tz).strftime('%Y-%m-%dT%H:00')
        times = hourly['time']
        
        # Find current hour index
        try:
            h_idx = times.index(current_time_str)
        except ValueError:
            h_idx = 0  # Fallback
            
        def extract_item(key, display_name):
            vals = hourly.get(key, [])
            unit = hourly_units.get(key, "")
            if not vals:
                return None
            valid_vals = [v for v in vals if v is not None]
            min_v = min(valid_vals) if valid_vals else 0
            max_v = max(valid_vals) if valid_vals else 0
            curr_v = vals[h_idx] if h_idx < len(vals) and vals[h_idx] is not None else 0
            return {
                'key': key,
                'name': display_name,
                'unit': unit,
                'current': curr_v,
                'min': min_v,
                'max': max_v,
                'hourly': vals
            }
            
        items = []
        items.append(extract_item('pm2_5', 'PM2.5'))
        items.append(extract_item('pm10', 'PM10'))
        items.append(extract_item('carbon_monoxide', 'CO'))
        items.append(extract_item('carbon_dioxide', 'CO2'))
        items.append(extract_item('nitrogen_dioxide', 'NO2'))
        items.append(extract_item('sulphur_dioxide', 'SO2'))
        items.append(extract_item('ozone', 'O3'))
        items.append(extract_item('methane', 'CH4'))
        
        return items
    except Exception as e:
        raise ParamError(f"Error parsing air quality data: {str(e)}")
