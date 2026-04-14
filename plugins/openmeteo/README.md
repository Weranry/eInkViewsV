# OpenMeteo 空气质量插件

此插件从 Open-Meteo 获取空气质量数据，支持 e-ink 屏幕渲染。

## 路由
- Air View: `/openmeteo/view/air?size=h2xl&lat=52.52&lon=13.41`
- Daily View: `/openmeteo/view/daily?size=hxl&lat=52.52&lon=13.41`
- Now View: `/openmeteo/view/now?size=h2xl&lat=52.52&lon=13.41`
- Tide View: `/openmeteo/view/tide?size=hxl&lat=52.52&lon=13.41`
- Soil View (土壤): `/openmeteo/view/soil?size=h2xl&lat=52.52&lon=13.41`
- Cloud View (云量): `/openmeteo/view/cloud?size=h2xl&lat=52.52&lon=13.41`

## 参数
- `lat`: 纬度
- `lon`: 经度
- `tz`: 时区 (默认 'Asia/Shanghai')

## 尺寸
- `h2xl` (400x300): 2x4 空气质量网格视图
