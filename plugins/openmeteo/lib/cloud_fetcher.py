import requests
from modules.errors.errors import ParamError

def fetch_cloud_data(lat, lon, tz='auto', timeout=5):
    """
    Fetch cloud cover at different altitudes.
    """
    if not lat or not lon:
        raise ParamError("Missing latitude or longitude")
        
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high",
        "timezone": tz
    }

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ParamError(f"fetch failed: {str(e)}")

    current = data.get("current", {})
    layers = [
        {"layer": "Total", "cover": current.get("cloud_cover")},
        {"layer": "High", "cover": current.get("cloud_cover_high")},
        {"layer": "Mid", "cover": current.get("cloud_cover_mid")},
        {"layer": "Low", "cover": current.get("cloud_cover_low")}
    ]
    
    return {"layers": layers}
