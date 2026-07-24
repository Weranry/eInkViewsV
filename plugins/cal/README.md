# cal - 日历插件

基于 lunar-python 的墨水屏日历视图插件，展示公历、农历、干支、节气、宜忌。

## 参数

本插件无需额外参数，默认显示当日/当月信息。

| 参数 | 必需 | 说明 |
| :--- | :--- | :--- |
| `size` | 是 | 视图尺寸，支持 `hxl`、`h2xl`、`h4xl` |

## 视图

### today - 今日

展示当日公历日期、农历日期、天干地支、生肖、节气、节日、宜忌。

### month - 月历

展示当月月历网格，包含公历日期、农历日期、节气标注、节日标注。

## 测试链接

```text
http://127.0.0.1:5000/cal/view/today?size=hxl
http://127.0.0.1:5000/cal/view/today?size=h2xl
http://127.0.0.1:5000/cal/view/month?size=hxl
http://127.0.0.1:5000/cal/view/month?size=h2xl
http://127.0.0.1:5000/cal/view/month?size=h4xl
```

## 依赖

- `lunar-python`：农历计算库

## 字体

- 正文：`assets/fonts/font.ttf`