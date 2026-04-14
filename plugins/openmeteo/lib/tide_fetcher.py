import requests
from modules.errors.errors import ParamError
from datetime import datetime
from modules.common_timezone import now_in_timezone

def degree_to_direction(deg):
    if deg is None:
        return "未知"
    directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
    idx = int((deg + 22.5) // 45) % 8
    return directions[idx]

def fetch_tide_data(lat, lon, tz='auto'):
    if not lat or not lon:
        raise ParamError("Coordinates (lat, lon) are strictly required.")
    
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wave_height,wave_period,wave_direction",
        "timezone": tz,
        "forecast_days": 2
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        # 针对Open-Meteo特殊的业务报错(如内陆无海洋数据)进行解析
        if response.status_code == 400:
            err_data = response.json()
            if err_data.get("error"):
                raise ParamError(f"Marine API Error: {err_data.get('reason', 'Invalid coordinates/Inland')}")
                
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise ParamError("Marine API Fetch Timeout (10s)")
    except requests.exceptions.ConnectionError:
        raise ParamError("Marine API Connection Failed")
    except requests.exceptions.HTTPError as e:
        raise ParamError(f"Marine API HTTP Error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise ParamError(f"fetch failed: {str(e)}")
        
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    wave_heights = hourly.get("wave_height", [])
    wave_periods = hourly.get("wave_period", [])
    wave_directions = hourly.get("wave_direction", [])
    
    local_now = now_in_timezone(tz)
    current_hour_str = local_now.strftime("%Y-%m-%dT%H:00")
    
    current_index = -1
    for i, t in enumerate(times):
        if t == current_hour_str:
            current_index = i
            break
            
    if current_index == -1:
         current_index = 0
         
    current_wave_height = wave_heights[current_index] if len(wave_heights) > current_index else None
    
    raw_period = wave_periods[current_index] if len(wave_periods) > current_index else None
    current_wave_period = f"{raw_period}秒" if raw_period is not None else "未知"
    
    raw_dir = wave_directions[current_index] if len(wave_directions) > current_index else None
    current_wave_direction = degree_to_direction(raw_dir)
    
    # Extract data for the next 24 hours (or available)
    start_idx = current_index
    end_idx = min(start_idx + 24, len(wave_heights))
    
    forecast_24h = []
    
    for i in range(start_idx, end_idx):
        if i < len(wave_heights) and wave_heights[i] is not None:
             forecast_24h.append(wave_heights[i])
             
    if not forecast_24h:
        raise ParamError("No wave height data (might be inland)")
        
    min_wave = min(forecast_24h)
    max_wave = max(forecast_24h)
    
    return {
        "current_wave_height": current_wave_height,
        "current_wave_period": current_wave_period,
        "current_wave_direction": current_wave_direction,
        "forecast_24h": forecast_24h,
        "min_wave": min_wave,
        "max_wave": max_wave,
        "update_time": local_now.strftime("%H:%M")
    }

