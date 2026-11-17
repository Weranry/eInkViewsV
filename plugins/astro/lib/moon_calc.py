"""月相计算：相位来自 JPL DE421 星历，由 Skyfield 读取仓库内 `assets/de421.bsp`。

相位角取「地心视角下月球与太阳的黄经之差」，恰好等于常见的月相定义：
0° = 新月、90° = 上弦、180° = 满月、270° = 下弦——与绘制模块（moon_phase）的约定一致。

所有计算都以 **UTC 时刻** 为准：相位只取决于绝对时刻，与观察者所在时区无关；
返回的 `next_new_moon` / `next_full_moon` 也是 UTC 时刻，由调用方按观察时区转换后展示。

星历文件缺失、或 Skyfield 不可用时，退回**平均朔望月线性外推**（误差约半天）：精简部署里
少了那 16MB 星历，插件也照样能出图，不至于直接报错。两条路径对外接口完全一致。
"""

import math
import os
import threading
from datetime import timezone, timedelta

from modules.utils import plog

# 星历放在仓库根的 assets/ 下；本文件位于 plugins/astro/lib/，往上三层即仓库根
_EPHEMERIS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'de421.bsp'))

# 退回近似算法时用到的常数：平均朔望月长度，与一个已知新月时刻（儒略日）
SYNODIC_MONTH = 29.530588853
REFERENCE_NEW_MOON_JD = 2451550.1

_load_lock = threading.Lock()
_kernel = None
_kernel_unavailable = False


def _as_utc(dt):
    """归一到 UTC 的 aware datetime；naive 输入按 UTC 解释。"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _get_phase_name(phase_angle):
    angle = phase_angle % 360
    if angle < 22.5:
        return 'New Moon'
    elif angle < 67.5:
        return 'Waxing Crescent'
    elif angle < 112.5:
        return 'First Quarter'
    elif angle < 157.5:
        return 'Waxing Gibbous'
    elif angle < 202.5:
        return 'Full Moon'
    elif angle < 247.5:
        return 'Waning Gibbous'
    elif angle < 292.5:
        return 'Last Quarter'
    elif angle < 337.5:
        return 'Waning Crescent'
    else:
        return 'New Moon'


def _load_kernel():
    """惰性加载星历，进程内长期复用；加载不了则返回 None（改走近似算法）。

    `load_file` 只是建立内存映射，几乎不耗时；`builtin=True` 让时间尺只用 Skyfield 自带的
    数据，不去联网抓闰秒与极移表——出图不依赖外网。
    """
    global _kernel, _kernel_unavailable
    if _kernel is None and not _kernel_unavailable:
        with _load_lock:
            if _kernel is None and not _kernel_unavailable:
                try:
                    from skyfield.api import load, load_file
                    from skyfield.framelib import ecliptic_frame
                    eph = load_file(_EPHEMERIS_PATH)
                    _kernel = (load.timescale(builtin=True), eph['earth'],
                               eph['moon'], eph['sun'], ecliptic_frame)
                except Exception as exc:
                    _kernel_unavailable = True
                    plog.warn(f'astro: 星历加载失败，退回平均朔望月近似（{_EPHEMERIS_PATH}）：{exc!r}')
    return _kernel


def _sky_phase_angle(kernel, dt):
    """地心视角下月球与太阳的黄经差（0=新月，90=上弦，180=满月，270=下弦）。"""
    ts, earth, moon, sun, frame = kernel
    e = earth.at(ts.from_datetime(dt))
    _, sun_lon, _ = e.observe(sun).apparent().frame_latlon(frame)
    _, moon_lon, _ = e.observe(moon).apparent().frame_latlon(frame)
    return (moon_lon.degrees - sun_lon.degrees) % 360.0


def _next_phase_time(kernel, dt, current_angle, target):
    """求下一次相位角等于 `target` 的 UTC 时刻。

    以平均朔望月估一个初值，再在初值 ±0.75 天内二分精修：相位在这段区间内单调递增，
    且真正落在其中，所以二分必然收敛到分钟级的准确时刻——不会和相位角两套口径打架。
    """
    offset = (target - current_angle) % 360.0
    guess = offset / 360.0 * SYNODIC_MONTH

    def residual(days):
        angle = _sky_phase_angle(kernel, dt + timedelta(days=days))
        return (angle - current_angle - offset + 180.0) % 360.0 - 180.0

    lo, hi = guess - 0.75, guess + 0.75
    for _ in range(18):
        mid = (lo + hi) / 2
        if residual(mid) < 0:
            lo = mid
        else:
            hi = mid
    return dt + timedelta(days=(lo + hi) / 2)


def _calc_analytic(dt):
    """退回路径：平均朔望月线性外推。返回 (相位角, 月龄, 下次新月, 下次满月)。"""
    jd = _datetime_to_jd(dt)
    moon_age = (jd - REFERENCE_NEW_MOON_JD) % SYNODIC_MONTH
    phase_angle = moon_age / SYNODIC_MONTH * 360.0
    next_new_moon = dt + timedelta(days=SYNODIC_MONTH - moon_age)
    if phase_angle < 180:
        days_to_full = (180 - phase_angle) / 360 * SYNODIC_MONTH
    else:
        days_to_full = (540 - phase_angle) / 360 * SYNODIC_MONTH
    return phase_angle, moon_age, next_new_moon, dt + timedelta(days=days_to_full)


def _datetime_to_jd(dt):
    """日期时间 → 儒略日（Meeus 标准算式），仅退回路径使用。"""
    wall = dt.replace(tzinfo=None)
    year, month = wall.year, wall.month
    day = wall.day + wall.hour / 24.0 + wall.minute / 1440.0 + wall.second / 86400.0 \
        + wall.microsecond / 86400000000.0
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) \
        + day + b - 1524.5


def calc_moon_phase(dt, lat=0.0):
    """计算 `dt`（UTC 时刻）在观测纬度 `lat` 下的月相。

    - `dt`：aware 或 naive（naive 按 UTC 解释）
    - `lat`：观测纬度，用于决定整轮月面的倾角
    - 返回的 `next_new_moon` / `next_full_moon` 为 UTC aware datetime
    """
    dt = _as_utc(dt)
    kernel = _load_kernel()

    if kernel is not None:
        phase_angle = _sky_phase_angle(kernel, dt)
        moon_age = phase_angle / 360.0 * SYNODIC_MONTH
        next_new_moon = _next_phase_time(kernel, dt, phase_angle, 0.0)
        next_full_moon = _next_phase_time(kernel, dt, phase_angle, 180.0)
    else:
        phase_angle, moon_age, next_new_moon, next_full_moon = _calc_analytic(dt)

    illumination = (1 - math.cos(math.radians(phase_angle))) / 2 * 100

    # 观测纬度决定整轮月面的倾角；南半球看到的月相上下颠倒，再翻转 180°
    rotation = -lat
    if lat < 0:
        rotation += 180.0

    return {
        'phase_angle': phase_angle,
        'illumination': illumination,
        'phase_name': _get_phase_name(phase_angle),
        'moon_age': moon_age,
        'next_new_moon': next_new_moon,
        'next_full_moon': next_full_moon,
        'rotation': rotation,
    }
