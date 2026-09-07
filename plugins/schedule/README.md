# 课程表插件 (Schedule Plugin)

将课程表数据渲染至墨水屏。经过 UI 深度重构，提供更符合 e-ink 屏幕特性的高清显示。

## 功能特性
- **UI 深度优化**：
  - 严格遵守 16 像素栅格对齐，消除锯齿和灰色虚边。
  - 强制 16 像素全周安全边距，确保文字永不超出屏幕边缘。
  - 使用明确的网格布局（标签列 / 内容列 / 信息列），支持竖向分栏线以增强可读性。
  - 每天固定展示 5 节课 (M1, M2, A1, A2, EV)，无课时保留空白行，不显示占位文本。
- **智能文本渲染**：
  - 课程名称自动带上《书名号》。
  - 内置 **自动换行引擎**，长课名会按列宽自动换行并在行高范围内完整显示，避免水平溢出。
  - 详细信息（教师/教室）自动右对齐，区分层级。
- **多尺寸支持**：全面适配横向、纵向主流墨水屏尺寸。

## 目录布局
- `assets/course/`: 存放课程表 JSON 文件。默认加载 `course_schedule.json`。
- `lib/fetcher.py`: 核心数据解析逻辑。
- `view/schedule_view/utils.py`: 布局与渲染核心工具类。
- `view/schedule_view/`: 渲染视图（hxl, h2xl, vxl, v2xl）。

## API 使用

### 1. 视图接口 (View)
`GET /schedule/view/schedule_view?size=<size_key>&json_name=<json_file_name>`

**支持的尺寸 (size)：**
- `hxl`: 横向 384x184 (4.2寸)
- `h2xl`: 横向 400x300 (4.2寸高清/7.5寸)
- `vxl`: 纵向 184x384 (4.2寸)
- `v2xl`: 纵向 300x400 (4.2寸高清/7.5寸)

**参数：**
- `json_name`: 可选，JSON 文件名（不含后缀）。默认值 `course_schedule`。
- `rotate`: 旋转角度 (0, c, cc, h)。
- `invert`: 是否反色 (t, f)。
- `tz`: 时区，默认 `Asia/Shanghai`。

**测试 URL 示例：**
- `http://127.0.0.1:5000/schedule/view/schedule_view?size=hxl`
- `http://127.0.0.1:5000/schedule/view/schedule_view?size=h2xl`
- `http://127.0.0.1:5000/schedule/view/schedule_view?size=vxl`
- `http://127.0.0.1:5000/schedule/view/schedule_view?size=v2xl`

### 2. 页面接口 (Page)
`GET /schedule/page/converter`

访问内置编辑器，生成符合格式的 JSON 文件。

## 注意事项 (Hardware Constraints)
- 为保护 e-ink 屏幕，所有渲染采用 Indexed 模式，仅支持 **黑、白、红** 三色。请勿输入包含渐变或半透明的内容。
- 所有数据拉取前建议先在 `converter.html` 预览 JSON 格式。

## 开发者
GitHub Copilot (Gemini 3 Flash Preview)

