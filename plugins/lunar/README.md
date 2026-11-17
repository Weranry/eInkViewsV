# Lunar (农历与日历) 插件说明文档

Lunar 插件提供了日历预览、黄历宜忌等多种功能，专为 e-ink 桌面看板或电子标签设计。

## API 接口信息

### 1. 日历视图 (rili)
提供包含公历、农历、干支纪年、节日等信息的综合日历视图。

**URL:** `/lunar/view/rili`

**支持参数:**
- `size`: 画布尺寸。支持: `h2xl`, `hxl`, `m`, `v2xl`, `vxl`
- `rotate`: 旋转 (`0`, `c`, `cc`, `h`)
- `invert`: 反转 (`t`, `f`)

**测试 URL:** `http://127.0.0.1:5000/lunar/view/rili?size=hxl`

### 2. 黄历视图 (huangli / huangliA)
提供基于中国传统黄历信息的宜忌展示。`huangliA` 为另一种布局风格。

**URL:** `/lunar/view/huangli` 或 `/lunar/view/huangliA`

**支持参数:**
- `size`: 支持 `hxl`, `h2xl`
- `rotate`: 旋转
- `invert`: 反转

**测试 URL:** `http://127.0.0.1:5000/lunar/view/huangli?size=hxl`

### 3. 日期数据接口 (JSON)
返回当前日期的结构化 JSON 数据。

**URL:** `/lunar/json/datejson`

## 功能说明
- **农历算法**: 内置精确的农历、干支算法库。
- **节日提醒**: 自动识别公历、农历传统节日。
- **精美排版**: 针对不同尺寸（横版、竖版、正方形）进行了自适应 UI 布局优化。

## 目录结构
- `json_module/`: 包含 `datejson.py`，提供数据接口。
- `lib/`: 包含黄历及日期计算的核心算法。
- `view/`: 包含 `rili`, `huangli`, `huangliA` 三种子路径，支持多种 e-ink 屏幕布局。
