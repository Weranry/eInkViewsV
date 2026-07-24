# Open-Meteo 天气插件

基于 Open-Meteo 免费天气 API 的墨水屏天气视图插件，展示当前天气信息。

## 参数

| 参数 | 必需 | 说明 |
| :--- | :--- | :--- |
| `lat` | 是 | 纬度，如 `31.23` |
| `lon` | 是 | 经度，如 `121.47` |
| `tz` | 是 | 时区，如 `Asia/Shanghai` |
| `size` | 是 | 视图尺寸，支持 `hxl`、`h2xl` |

## 视图

### now - 当前天气

展示当前温度、体感温度、天气状况、湿度、风速风向、气压。

### forecast - 逐日预报

展示未来多日天气预报，包含天气图标、最高/最低温度、降水概率。

## 测试链接

```text
http://127.0.0.1:5000/openmeteo/view/now?size=hxl&lat=31.23&lon=121.47&tz=Asia/Shanghai
http://127.0.0.1:5000/openmeteo/view/now?size=h2xl&lat=31.23&lon=121.47&tz=Asia/Shanghai
http://127.0.0.1:5000/openmeteo/view/forecast?size=hxl&lat=31.23&lon=121.47&tz=Asia/Shanghai
http://127.0.0.1:5000/openmeteo/view/forecast?size=h2xl&lat=31.23&lon=121.47&tz=Asia/Shanghai
```

## 天气代码对照

| 代码 | 描述 |
| :--- | :--- |
| 0 | 晴 |
| 1-2 | 少云/多云 |
| 3 | 阴 |
| 45, 48 | 雾 |
| 51-55 | 毛毛雨 |
| 61-65 | 雨 |
| 71-77 | 雪 |
| 80-82 | 阵雨 |
| 85-86 | 阵雪 |
| 95-99 | 雷暴 |

## 字体

- 正文：`assets/fonts/font.ttf`
- 天气图标：`assets/fonts/weather-icon.ttf`