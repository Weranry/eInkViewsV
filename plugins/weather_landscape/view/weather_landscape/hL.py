from .utils import prepare_canvas, finalize_image
from ...lib.weather_landscape_fetcher import WeatherData
from ...lib.weather_landscape_view import WeatherDrawer

def generate_image(lat: float = 0.0,
                   lon: float = 0.0,
                   key: str = '',
                   units: int = 0,
                   pressure_min: float = 980.0,
                   pressure_max: float = 1030.0,
                   rotate: int = 0,
                   invert: bool = False,
                   cmode=None,
                   **kwargs):
    try:
        lat = float(lat)
    except Exception:
        lat = 0.0
    try:
        lon = float(lon)
    except Exception:
        lon = 0.0
    try:
        units = int(units)
    except Exception:
        units = 0
    try:
        pressure_min = float(pressure_min)
        pressure_max = float(pressure_max)
    except Exception:
        pressure_min = 980.0
        pressure_max = 1030.0

    weather_data = WeatherData(key, lat, lon, units_mode=units,
                               pressure_min=pressure_min, pressure_max=pressure_max)
    weather_data.get_weather_data()

    drawer = WeatherDrawer()
    # 规范尺寸
    drawer.IMAGE_WIDTH = 250
    drawer.IMAGE_HEIGHT = 122
    drawer.DRAWOFFSET = 60
    drawer.XSTART = 32
    drawer.XSTEP = 44
    drawer.XFLAT = 10
    drawer.YSTEP = 50
    drawer.DEFAULT_DEGREE_PER_PIXEL = 0.5
    drawer.FLOWER_LEFT_PX = 10
    drawer.FLOWER_RIGHT_PX = 15

    # 使用 prepare_canvas 创建画布
    img, _ = prepare_canvas('hL', palette_type='bw', cmode=cmode)
    img_drawn = drawer.draw_weather(weather_data)
    return finalize_image(img_drawn, rotate=rotate, invert=invert)
