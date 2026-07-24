# Dashboard 综合信息仪表盘

## 简介
800x480 (h4xl) 墨水屏综合信息仪表盘，集成日历、天气、未来三日预报、一言、新闻、历史上的今天六大模块。

## 数据来源
- **日历**: `lunar-python` 库，提供公历、农历、干支、节气、宜忌、生肖
- **天气**: Open-Meteo API，提供实时天气 + 未来三日预报
- **一言**: Hitokoto API (v1.hitokoto.cn)
- **新闻**: RSS 抓取（人民网、新华网、环球网）
- **历史**: Wikipedia "On This Day" API（中文优先，英文 fallback）

## 参数
| 参数 | 类型 | 必需 | 说明 |
| :--- | :--- | :--- | :--- |
| `lat` | float | 是 | 纬度 |
| `lon` | float | 是 | 经度 |
| `tz` | string | 是 | 时区，如 `Asia/Shanghai` |

## 视图
| 视图 | 尺寸 | 路径 |
| :--- | :--- | :--- |
| overview | 800x480 | `/dashboard/view/overview?size=h4xl` |

## 测试链接
```
http://127.0.0.1:5000/dashboard/view/overview?size=h4xl&lat=39.9042&lon=116.4074&tz=Asia/Shanghai
```