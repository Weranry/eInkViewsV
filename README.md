
# eInkViews

---

## 项目简介
eInkViews 是为 [Open ePaper Link](https://openepaperlink.org) 设计的墨水屏图像渲染与分发服务，基于 Flask，支持插件化扩展，适配多种尺寸和多色电子纸硬件。

## 主要特性
- 插件化架构，灵活扩展
- Pillow 动态渲染，像素级排版
- 多色支持与降级（通过 `cmode` 参数适配不同硬件）
- 多尺寸/方向适配，支持旋转、反色
- Unicode 字符与复杂排版支持
- 云端一键部署（Vercel）

---

## 快速上手
1. 克隆仓库并安装依赖：
	```bash
	git clone https://github.com/Weranry/eInkViews.git
	cd eInkViews
	pip install -r requirements.txt
	```
2. 安装插件：将自定义或第三方插件目录放入 `plugins/` 文件夹。
3. 本地启动：
	```bash
	python -B test.py
	```
	访问 `http://127.0.0.1:5000` 进行调试。
4. 部署到 Vercel：导入 GitHub 仓库，自动识别 `vercel.json`。

---

## 接口与参数说明

### 1. 路由规范
| 类型 | 路由格式 | 说明 |
| :--- | :--- | :--- |
| 视图 (View) | `/{plugin}/view/{kind}?size=hxl` | 返回生成的图像 (JPEG) |
| 数据 (JSON) | `/{plugin}/json/{name}` | 返回插件抓取的原始 JSON |
| 工具 (Page) | `/{plugin}/page/{name}` | 插件自带 HTML 配置/说明页 |
| 随机 (Random) | `/random/views?routes=...` | 多视图权重轮播/随机展示 |

### 2. 公共参数（Query Parameters）
| 参数 | 选项 | 说明 |
| :--- | :--- | :--- |
| size | m, hl, hxl, h2xl... | 详见下表 |
| rotate | 0, c, cc, h | 旋转：无/顺时针90°/逆时针90°/180° |
| invert | t, f | 反色：黑白像素取反 |
| cmode | 2bw, r2y, y2r, yr2r, yr2y | 颜色降级，见下 |
| tz | Asia/Shanghai... | 时区设置 |

#### cmode 颜色降级模式
| cmode | 效果 |
| :--- | :--- |
| None | 保持原调色板（支持多色） |
| 2bw | 所有非白像素转黑，仅黑白两色 |
| r2y | 红色转黄色 |
| y2r | 黄色转红色 |
| yr2r | 红色和黄色都转红色 |
| yr2y | 红色和黄色都转黄色 |

---

## 尺寸对照表
| Key | 物理尺寸 | 分辨率 | 推荐型号 |
| :--- | :--- | :--- | :--- |
| m | 1.54" | 200x200 | 通用方屏 |
| hl / vl | 2.13" | 250x122 / 122x250 | 电子价签标准版 |
| hxl / vxl | 3.50" | 384x184 / 184x384 | 中型信息屏 |
| h2xl / v2xl | 4.20" | 400x300 / 300x400 | 桌面仪表盘 |
| h4xl / v4xl | 7.50" | 800x480 / 480x800 | 大型看板 |

---

## 插件开发建议

建议插件遵循如下结构以便自动装载：
```text
plugins/your_plugin/
├── lib/               # 业务逻辑（如数据抓取、解析）
├── view/              # 视图层，负责 Pillow 绘图逻辑
│   └── kind_name/     # 视图种类 (如: air, daily)
│       ├── utils.py   # 可选：该种类视图公用的坐标计算、复杂图形绘制函数
│       ├── hxl.py     # 横屏 3.5" 布局
│       └── h2xl.py    # 横屏 4.2" 布局
├── json_module/       # 可选：原始数据接口模块
├── page/              # 可选：插件配置、说明或交互 HTML 页面
├── plugin_config.py   # 可选：插件默认配置项
└── routes.py          # 核心路由注册
```

---

## 开发注意事项

- 建议插件优先使用标准调色板（如 bwr、bwy、bwry、7color），框架会自动降级。
- 字体建议为 16 的整数倍，优先用 `draw.textbbox()` 动态计算文本边界。
- 建议文本内容距离画布边缘至少 2px。
- 网络请求建议放在 lib/，并设置 timeout。
- 数据抓取失败建议抛出 ParamError，框架会返回 JSON 错误。
- 不同尺寸建议单独布局，避免直接拉伸。
- 资源路径建议用 `os.path.join(os.path.dirname(__file__), ...)`，适配多环境。
- `generate_image` 建议在 create_canvas 前完成数据采集。
- 不建议直接修改 modules/ 公共库，特殊逻辑可在插件内部实现。
- 文件名建议小写，保证跨平台兼容。

---

## 开源协议
本项目采用 [MIT License](LICENSE) 开源。
© 2024-2026 Made by [Weranry](https://github.com/Weranry)
