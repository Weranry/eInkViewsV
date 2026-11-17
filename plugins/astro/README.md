# Astro - 天文月相插件

通过经纬度返回当前月相图案和详细信息的墨水屏视图。

## 配置参数 (DEFAULT_ARGS)

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `lat` | float | None | 观测纬度，与 lon 同时提供 |
| `lon` | float | None | 观测经度，与 lat 同时提供 |
| `tz` | str | UTC | 时区，支持数值偏移(如 `8`)或 IANA 名称(如 `Asia/Shanghai`) |

## 视图

### phase - 月相视图

显示当前月相图案、相位名称、照明度、月龄、下一次新月和满月时间。

## 测试链接

- hxl (384×184): `http://127.0.0.1:5000/astro/view/phase?size=hxl&lat=31.23&lon=121.47&tz=Asia/Shanghai`
- h2xl (400×300): `http://127.0.0.1:5000/astro/view/phase?size=h2xl&lat=31.23&lon=121.47&tz=Asia/Shanghai`

## 目录结构

```
plugins/astro/
├── __init__.py
├── plugin_config.py       # 默认参数
├── routes.py              # 路由注册
├── lib/
│   └── moon_calc.py       # 月相计算（Skyfield 读 assets/de421.bsp 星历）
└── view/
    └── phase/
        ├── hxl.py         # 3.5" 横屏 (384×184)
        └── h2xl.py        # 4.2" 横屏 (400×300)
```

月相**绘制**逻辑不放在插件里，而是复用框架模块
`modules/generate_views/moon_phase.py`——它是纯函数、不依赖插件框架，其他插件也能直接用：

```python
from modules.generate_views.moon_phase import draw_moon_sprite

sprite = draw_moon_sprite(phase_angle, size=170, rotation=rotation)  # → RGBA 精灵
img.paste(1, (x, y), mask=sprite.split()[3])
```

## 精度与星历

相位由 **JPL DE421 星历**经 Skyfield 计算：取地心视角下月球与太阳的黄经之差作为相位角
（0°=新月、90°=上弦、180°=满月、270°=下弦），「下次新月 / 满月」也用星历二分求准到分钟级。
星历文件是仓库根 `assets/de421.bsp`（约 16 MB），离线读取、不联网；依赖见 `requirements.txt`
的 `skyfield`。

星历缺失或 Skyfield 不可用时，`moon_calc.py` 退回**平均朔望月线性外推**（误差约 ±0.5 天），
插件照常出图，两条路径对外接口一致。