# Weather Landscape 插件说明文档

此插件基于 OpenWeatherMap API 提供精美的动态风景天气视图，支持将实时的气压、温度、云量、雨雪等信息转化为 e-ink 画布点阵图像。

## API 接口信息

### 1. 天气渲染视图 (View)
该接口返回 24位 RGB 图像，经过 base-line JPEG 处理，专为 e-ink 屏幕驱动优化。

**URL:** `/<plugin_name>/view/weather_landscape`

**支持参数:**
| 参数名 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `size` | string | **必填** | 画布尺寸。支持: `hL`(250x122), `hxl`(384x184), `hp` |
| `lat` | float | `0.0` | 纬度坐标 |
| `lon` | float | `0.0` | 经度坐标 |
| `key` | string | `''` | OpenWeatherMap API Key (必填) |
| `units` | int | `0` | 温度单位: `0`-摄氏度, `1`-华氏度 |
| `rotate` | string | `0` | 旋转方向: `0`, `c`(顺时针), `cc`(逆时针), `h`(180度) |
| `invert` | string | `f` | 颜色反转: `t`(开启), `f`(关闭) |
| `cmode` | string | `None` | 自定义调色板处理模式 |

**使用示例:**
`http://127.0.0.1:5000/weather_landscape/view/weather_landscape?size=hL&lat=36.7066&lon=119.1268&key=d1012395b4ad93ba5388e78e3f0cfd9f`

## 功能特性
- **动态气压烟雾**: 壁炉烟雾倾角随当地气压实时调整。
- **动态降水系统**: 根据实时降雨量/降雪量在画面中渲染对应的雨线或雪花标识。
- **云量显示**: 自动根据天空云量百分比显示对应档位的云朵图像。
- **精细渲染**: 采用贝塞尔曲线平滑处理温度趋势，集成专用 Sprites 库。

## 目录结构
- `lib/`: 包含 `weather_landscape_fetcher.py` (数据抓取) 和 `weather_landscape_view.py` (绘制逻辑)。
- `assets/sprite/`: 存储天气图标点阵资源。
- `view/weather_landscape/`: 存放各尺寸的具体布局配置。
