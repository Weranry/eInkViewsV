# eInkViews

eInkViews 是为 Open ePaper Link 设计的墨水屏图像渲染与分发服务，基于 Flask 构建，采用插件化架构，使用 Pillow 进行像素级排版与图像生成，面向多尺寸、多色电子纸硬件输出 JPEG 图像。

## 项目定位

这个项目的目标不是通用 Web UI，而是面向墨水屏硬件的渲染和分发中枢。它负责：

- 从插件中获取数据
- 按尺寸和调色板生成图像
- 提供 RESTful API 给设备或其他系统拉取
- 支持 Vercel Serverless 部署

## 核心特性

- 插件化架构，支持自动发现与自动注册
- 多尺寸适配，覆盖横屏和竖屏的常见墨水屏规格
- 多色支持与降级，兼容 bw、bwr、bwy、bwry、7color
- 支持旋转、反色和调色板映射
- 支持 Unicode、TrueType 字体和精确排版
- 支持 JSON、HTML 页面和随机视图路由
- 内置 EVKEY 鉴权
- 可直接部署到 Vercel

## 路由概览

| 类型 | 路由 | 说明 |
| :--- | :--- | :--- |
| 视图 | `/{plugin}/view/{kind}?size=hxl` | 返回生成的 JPEG 图像 |
| JSON | `/{plugin}/json/{name}` | 返回插件原始数据或结构化结果 |
| 页面 | `/{plugin}/page/{name}` | 返回插件自带 HTML 页面 |
| 随机视图 | `/random/views?routes=...` | 支持加权随机选择多个视图 |
| 首页 | `/` | 项目欢迎页 |
| 图标 | `/favicon.ico` | 网站图标 |

## 公共查询参数

| 参数 | 可选值 | 说明 |
| :--- | :--- | :--- |
| `size` | `m, hl, hxl, h2xl, h3xl, h4xl, vl, vxl, v2xl, v3xl, v4xl` | 预定义画布尺寸 |
| `rotate` | `0, c, cc, h` | 旋转：无、顺时针 90°、逆时针 90°、180° |
| `invert` | `t, f` | 是否反色 |
| `cmode` | `2bw, r2y, y2r, yr2r, yr2y` | 调色板降级模式 |
| `tz` | 如 `Asia/Shanghai` | 时区参数 |
| `evkey` | 字符串 | 鉴权密钥 |

注意：测试链接和文档示例中不要带 `palette` 参数，调色板应在代码中固定，不通过 GET 传递。

## 目录结构

```text
eInkViews/
├── app.py
├── test.py
├── config.py
├── requirements.txt
├── vercel.json
├── public/
│   ├── pages/
│   └── favicon.ico
├── assets/
│   └── fonts/
├── modules/
│   ├── errors/
│   ├── generate_views/
│   ├── plugins/
│   ├── register/
│   ├── common_timezone.py
│   ├── evkey_auth.py
│   └── test_core.py
└── plugins/
	└── your_plugin/
		├── __init__.py
		├── routes.py
		├── plugin_config.py
		├── lib/
		├── json_module/
		├── page/
		└── view/
			└── <kind>/
				├── hxl.py
				├── h2xl.py
				└── utils.py
```

## 核心模块说明

### 入口文件

- `app.py`：生产入口，创建 Flask 应用并注册插件、错误处理、随机路由和首页路由
- `test.py`：本地调试入口，建议使用 `python -B test.py` 运行

### 配置文件

- `config.py`：全局默认配置，如旋转、反色、图像质量、时区、鉴权开关和白名单

### 图像生成模块

| 模块 | 职责 |
| :--- | :--- |
| `modules/generate_views/canvas_factory.py` | 创建画布、定义尺寸和调色板、完成最终图像处理 |
| `modules/generate_views/font_loader.py` | 加载全局字体和插件字体 |
| `modules/generate_views/image_transform.py` | 旋转、反色等图像处理 |
| `modules/generate_views/palette_mapper.py` | 调色板降级映射 |
| `modules/generate_views/qrcode_util.py` | 生成二维码 |
| `modules/generate_views/random_image.py` | 动态加载插件视图模块 |

### 注册与基础设施模块

| 模块 | 职责 |
| :--- | :--- |
| `modules/register/auto_view_routes.py` | 自动注册视图路由 |
| `modules/register/auto_json_routes.py` | 自动注册 JSON 路由 |
| `modules/register/auto_page_routes.py` | 自动注册页面路由 |
| `modules/register/random_view_route.py` | 随机视图路由 |
| `modules/register/template_routes.py` | 首页与图标路由 |
| `modules/plugins/plugin_loader.py` | 自动发现并注册插件 |
| `modules/plugins/__init__.py` | 加载插件配置并缓存 |
| `modules/errors/errors.py` | 自定义异常与全局错误处理 |
| `modules/common_timezone.py` | 时区换算工具 |
| `modules/evkey_auth.py` | EVKEY 鉴权中间件 |

## 尺寸对照表

| Key | 分辨率 | 物理尺寸 | 方向 |
| :--- | :--- | :--- | :--- |
| `m` | 200×200 | 1.54" | 不分横竖 |
| `hl` | 250×122 | 2.13" | 横屏 |
| `hxl` | 384×184 | 3.50" | 横屏 |
| `h2xl` | 400×300 | 4.20" | 横屏 |
| `h3xl` | 600×480 | 5.83" | 横屏 |
| `h4xl` | 800×480 | 7.50" | 横屏 |
| `vl` | 122×250 | 2.13" | 竖屏 |
| `vxl` | 184×384 | 3.50" | 竖屏 |
| `v2xl` | 300×400 | 4.20" | 竖屏 |
| `v3xl` | 480×600 | 5.83" | 竖屏 |
| `v4xl` | 480×800 | 7.50" | 竖屏 |

## 调色板说明

| Key | 颜色组成 | 说明 |
| :--- | :--- | :--- |
| `bw` | 白 + 黑 | 双色屏 |
| `bwr` | 白 + 黑 + 红 | 三色屏 |
| `bwy` | 白 + 黑 + 黄 | 三色屏 |
| `bwry` | 白 + 黑 + 红 + 黄 | 四色屏 |
| `7color` | 白 + 黑 + 红 + 黄 + 绿 + 蓝 + 橙 | 七色屏 |

`cmode` 用于在返回图片前按规则重新映射颜色：

- `2bw`：所有非白色降为黑色
- `r2y`：红转黄
- `y2r`：黄转红
- `yr2r`：红黄都转红
- `yr2y`：红黄都转黄

## 插件开发约定

每个插件建议遵循以下结构：

```text
plugins/your_plugin/
├── __init__.py
├── README.md
├── plugin_config.py
├── routes.py
├── lib/
├── json_module/
├── page/
└── view/
	└── <kind>/
		├── hxl.py
		├── h2xl.py
		└── utils.py
```

### routes.py

插件路由入口必须定义：

- `PLUGIN_NAME`
- `PLUGIN_DESCRIPTION`
- `bp` 蓝图对象

并通过自动路由注册插件视图、JSON 和页面。

### plugin_config.py

插件配置文件用于定义：

- 插件元数据
- `DEFAULT_ARGS`
- 可选的 `DEFAULT_ROTATE`
- 可选的 `DEFAULT_INVERT`

### lib/

- 数据获取和清洗优先在 `lib/` 中完成
- 每个视图种类建议对应一个独立模块
- 所有网络请求必须设置 `timeout`
- 数据获取失败时抛出 `ParamError`、`AuthError` 或 `NotFoundError`
- 不要在这里写本地临时文件，尽量使用 `io.BytesIO`

### view/<kind>/<size>.py

视图文件必须满足以下要求：

- 文件顶部包含路径兼容处理
- 函数签名统一为 `generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs)`
- 视图层只负责渲染，不负责参数降级或默认值补全
- 先拿到数据，再创建画布
- 使用 `draw.textbbox()` 动态测量文本尺寸
- 黑色必须显式使用 `fill=1` 或 `fill=(0, 0, 0)`，不要使用 `fill=0`
- 默认提供 `hxl` 和 `h2xl` 两个横屏尺寸实现，除非用户明确指定其他尺寸

### 视觉规范

- 默认采用航空电子仪表风格，强调清晰、克制、分层明确
- 主标题和大数值建议使用 32px 及以上字号，次级信息建议 16px
- 所有字号尽量使用 16 的整数倍
- 所有文字、线条和图形绘制前都要检查边界，避免溢出
- 如果插入位图，必须使用 Floyd-Steinberg 抖动

## 插件参数类型

| 类型 | 典型插件 | 必需参数 | 说明 |
| :--- | :--- | :--- | :--- |
| 地理位置相关 | `openmeteo`、`lunar`、`ics_calendar` | `lat`、`lon`、`tz` | 任一坐标存在时，两个坐标都必须提供 |
| 用户标识相关 | `github` | `username` | 需要在路由或 lib 中校验非空 |
| 内容选择相关 | `hitokoto` | 无 | 仅透传如 `category`、`c`、`type` 等参数 |
| 资源文件相关 | `schedule` | `json_name` | 不存在时返回 `NotFoundError` |
| 纯内容插件 | `zhihu`、`news` | 无 | 无需额外参数 |

## 插件开发参考

如果你要新写一个插件，可以直接参考 [plugin_template/README.md](plugin_template/README.md) 的骨架，再对照 [lunar/README.md](lunar/README.md) 的真实写法做替换。

### 参考结构

`lunar` 是一个很适合照着写的例子，它把“数据计算、JSON 接口、双尺寸视图”分得很清楚：

- `routes.py` 负责注册蓝图、视图路由和 JSON 路由
- `plugin_config.py` 负责插件名、描述和默认参数
- `lib/date_calculator.py` 负责公历、农历、干支、节气和节日数据
- `json_module/datejson.py` 负责输出结构化日期数据
- `view/rili/` 负责日历视图
- `view/huangli/` 负责黄历视图
- `view/huanglia/` 负责另一套黄历布局

### 视图写法

`lunar` 的视图结构可以直接概括成下面这个模式：

1. 先从 `lib/` 拿到完整数据
2. 再用 `create_canvas(size_key, 'bwr', cmode=cmode)` 创建画布
3. 在 `hxl` 和 `h2xl` 两个文件里分别写独立布局
4. 最后统一调用 `finalize_image_common(img, rotate=rotate, invert=invert)` 返回结果

### 插件模板

`plugin_template/` 是一个可直接复制的模板目录，已经按 `lunar` 的结构预留了：

- `rili` 和 `huangli` 两个示例视图目录
- `lib/date_calculator.py` 的数据占位
- `json_module/datejson.py` 的 JSON 入口
- `routes.py` 和 `plugin_config.py` 的标准骨架

你创建新插件时，可以先复制这个目录，再把里面的 `your_plugin`、`rili`、`huangli` 和示例数据替换成自己的业务内容。

## 参数优先级

参数合并遵循以下优先级：

```text
URL 显式参数 > 插件 plugin_config.py 默认值 > 全局 config.py 默认值
```

常见参数包括：`rotate`、`invert`、`cmode` 和插件业务参数。

## 开发与测试

本项目建议使用下面的方式进行本地调试：

```bash
python -B test.py
```

不要使用 `app.py` 作为开发测试入口。`app.py` 主要面向生产和 Vercel 部署。

### 测试链接格式

测试时请使用完整 URL，不要使用相对路径，也不要带 `palette` 参数：

- 地理位置类：`http://127.0.0.1:5000/openmeteo/view/now?size=hxl&lat=31.23&lon=121.47&tz=Asia/Shanghai`
- 用户标识类：`http://127.0.0.1:5000/github/view/dashboard?size=hxl&username=octocat`
- 内容选择类：`http://127.0.0.1:5000/hitokoto/view/quote?size=hxl`
- 资源文件类：`http://127.0.0.1:5000/schedule/view/schedule_view?size=hxl`
- 纯内容类：`http://127.0.0.1:5000/zhihu/view/daily?size=hxl`

## 部署说明

### 本地运行

1. 安装依赖
2. 将插件放入 `plugins/`
3. 执行 `python -B test.py`
4. 在浏览器访问 `http://127.0.0.1:5000`

### Vercel 部署

- 保持无状态设计，不要写本地临时文件
- 所有资源路径使用 `os.path.join(os.path.dirname(__file__), ...)`
- 避免模块顶层做重计算，优先懒加载
- 路由配置需与 Flask 路由一致

## 约束与禁用项

- 不要在视图层做参数降级或默认值补全
- 不要在测试中使用 `app.py`
- 不要创建或激活虚拟环境
- 不要引入不在 `requirements.txt` 中的第三方包
- 不要生成 `__pycache__`，所有 Python 命令请带 `-B`
- 不要把测试链接写成相对路径
- 不要在测试链接里加入 `palette`
- 不要把黑色绘制写成 `fill=0`
- 不要把图片输出到 `plugins/` 或根目录散落位置，统一放到 `output/`

## 维护提示

当修改核心框架、插件规则或路由规范时，要同步更新这份 README，避免文档与实际行为脱节。插件开发时尤其要保证：

- 视图模块与尺寸规范一致
- `README.md` 与参数、预览链接同步
- 每个新视图种类都有独立的 `lib` 模块
- 所有网络请求都带 `timeout`
- 所有绘图都先检查边界


