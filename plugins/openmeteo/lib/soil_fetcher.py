import requests
from modules.errors.errors import ParamError

def fetch_soil_data(lat, lon, tz='auto', timeout=5):
    """
    Fetch soil temperature and moisture at different depths.
    """
    if not lat or not lon:
        raise ParamError("Missing latitude or longitude")
        
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "soil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_9_to_27cm,soil_moisture_27_to_81cm",
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
        {
            "depth": "0cm",
            "temperature": current.get("soil_temperature_0cm"),
            "moisture": current.get("soil_moisture_0_to_1cm")
        },
        {
            "depth": "6cm",
            "temperature": current.get("soil_temperature_6cm"),
            "moisture": current.get("soil_moisture_1_to_3cm")
        },
        {
            "depth": "18cm",
            "temperature": current.get("soil_temperature_18cm"),
            "moisture": current.get("soil_moisture_9_to_27cm")
        },
        {
            "depth": "54cm",
            "temperature": current.get("soil_temperature_54cm"),
            "moisture": current.get("soil_moisture_27_to_81cm")
        }
    ]
    
    return {"layers": layers}
