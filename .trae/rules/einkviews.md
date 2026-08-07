---
alwaysApply: true
name: "eInkViews Rules"
description: "Consolidated hard rules for all eInkViews agents and skills. Use this as the single source of truth for layout, deployment, testing, and parameter handling."
---

# eInkViews 统一规则

## 1. 适用范围

本文件只保留硬性规则。任何 Agent / Skill / 任务说明都不得与这里冲突。

## 2. 绝对约束

- 项目运行在 Vercel Serverless 环境，禁止本地临时文件写入，图像处理优先使用 `io.BytesIO`
- 禁止使用 `app.logger.exception()`，改用 `print()` 或 `traceback.print_exc()`
- 所有 Python 命令必须带 `-B`，禁止生成 `__pycache__`
- 禁止创建或激活虚拟环境
- 禁止引入 `requirements.txt` 之外的第三方包
- 测试入口只能是 `test.py`，禁止把 `app.py` 当测试入口，无论什么情况，必须使用 `test.py`测试
- 路径必须使用 `os.path.join(os.path.dirname(__file__), ...)`
- 黑色必须显式写 `fill=1` 或 `fill=(0,0,0)`，禁止用 `fill=0`
- 所有视图必须先拿到数据，再创建画布
- 所有文本测量必须使用 `draw.textbbox()`
- 任何元素绘制前都必须做边界检查，禁止越界硬画
- 测试链接必须是完整 URL，格式为 `http://127.0.0.1:5000/...`
- 测试链接中禁止包含 `palette` 参数
- 一个视图种类对应一个lib中的模块，不能多视图种类一个模块。

## 3. 视图与排版规则

- 默认只做横屏视图，除非用户明确要求竖屏
- 同一视图种类必须分别实现 `hxl` 和 `h2xl`
- `h2xl` 必须独立布局，不能简单缩放 `hxl`
- 核心标题或大数值建议 32px 以上
- 次要信息建议 16px
- 字号必须强制使用使用 16 的整数倍，没得商量
- 画面要分区清晰、留白充足、信息密度适中
- 红色只用于标题、警示或核心数据，不要滥用
- 位图插入必须使用 Floyd-Steinberg 抖动
- 不同尺寸的视图必须分别实现，不能简单缩放其他尺寸，可以对视图的详细程度进行调整，比如大视图可以展示更多详细信息，但是一个视图对应一个lib中的模块，你可以多获取信息，但是不一定都要展示出来，根据实际情况判断是否展示。

## 4. 参数规则

参数优先级固定为：URL 显式参数 > 插件 `plugin_config.py` 默认值 > 全局 `config.py` 默认值。

常见参数按插件类型处理：

| 类型 | 必需参数 | 说明 |
| :--- | :--- | :--- |
| 地理位置类 | `lat`, `lon`, `tz` | 任一出现则三者都要齐 |
| 用户标识类 | `username` | 在路由层或 lib 层校验非空 |
| 内容选择类 | 无 | 直接透传给 API |
| 资源文件类 | `json_name` | 文件不存在返回 `NotFoundError` |
| 纯内容类 | 无 | 不做额外参数校验 |

## 5. 字体与资源

- 全局字体只从项目根目录 `assets/fonts/` 读取
- 插件私有字体只从插件自己的 `assets/fonts/` 读取
- 只有确认文件真实存在时才引用字体，不要凭空编造文件名
- 图标优先使用字体图标，不优先使用位图

## 6. 最小验收清单

- [ ] 路由、参数、视图、README 已同步
- [ ] 画布创建前已完成数据获取
- [ ] 所有文本都有边界检查
- [ ] hxl / h2xl 都已实现
- [ ] 测试链接是完整 URL，且不含 palette

