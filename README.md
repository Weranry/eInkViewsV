# eInkViews
## 项目介绍
---
**eInkViews** 是一个为 [Open ePaper Link](https://openepaperlink.org) 项目中 `image_url` 功能设计的墨水屏图像信息展示服务，支持插件化扩展。它可灵活适配多种尺寸墨水屏，通过 pillow 库动态生成图片，也可直接返回对应的 Json 数据可按需调用。

eInkViews 基于 [ePapaer DashBoard](https://github.com/weranry/epaperdashboard) 升级而来，增加了插件化扩展功能，可灵活增减模块，并对图像绘制等代码进行了抽象，专注于信息与图像排版设计，解决了单片机驱动墨水屏展示大量信息的困难，以及 Open ePaper Link 不支持复杂排版和 Unicode 字符的问题。

## 快速开始
---
### 拉取代码
```bash
git clone https://github.com/Weranry/eInkViews.git
cd eInkViews
```
### 安装依赖
```bash
pip install -r requirements.txt
```
### 启动服务
```bash
python app.py
```

## 项目结构
---
```
/eInkViews/
├── app.py # 项目主程序入口
├── config.py # 项目配置文件
├── requirements.txt # 项目依赖
├── vercel.json # Vercel部署配置
├── public/ # 静态资源公共目录
│ ├── pages # 项目前端页面
│ └── favicon.ico # 项目图标
├── modules/ # 核心功能模块目录
│ ├── errors/ # 错误处理
│ ├── generate_views/ # 视图生成
│ ├── plugins/ # 插件管理
│ ├── register/ # 路由注册
│ └── templates/ # 模板路由
└── plugins/ # 插件目录
├── plugins_A # 插件A
├── plugins_B # 插件B
└── ... # 更多插件
```

## 路由与参数
---
### Views 视图接口
```
GET /{plugin_name}/view/{view_name}?size={size}&rotate={r}&invert={i}&param=value...
```
- **plugin_name**：插件名称
- **view_name**：插件下的视图名称

#### 尺寸 size 参数

|标识|尺寸|方向|
|---|---|---|
|m|200x200|无|
|hL|250x122|横向|
|hxl|384x184|横向|
|h2xl|400x300|横向|
|h3xl|600x480|横向|
|h4xl|800x480|横向|
|vL|122x250|纵向|
|vxl|184x384|纵向|
|v2xl|300x400|纵向|
|v3xl|480x600|纵向|
|v4xl|480x800|纵向|

#### 旋转 rotate 参数

- `rotate`：旋转角度，支持 `c`(顺时针90°)、`cc`(逆时针90°)、`h`(180°)、`0`(默认)

#### 反色 invert 参数
- `invert`：反色，`t`(是)、`f`(否)

#### 颜色 cmode 参数
- 
  

### 2. JSON 数据接口
```
GET /{plugin_name}/json/{json_name}?param=value
```

- **plugin_name**：插件名称
- **json_name**：插件中的 JSON 格式名称
- **params**：由具体模块定义

  

#### 相关配置（config.py）
- `MODULE_IMPORT_CACHE_SIZE`：JSON模块导入缓存数量，默认 256


### 3. 页面接口
```
GET /{plugin_name}/page/{page_name}
```
- **plugin_name**：插件名称
- **page_name**：插件中 pages/ 目录下的页面名称

页面可以是静态HTML，可用于提供插件的工具和文档。

  

### 4. Random Views 视图接口
```
GET /random/views?routes={路由描述串}&rotate={r}&invert={i}

```

- **路由描述串**：格式为 `plugin_name.view_name[:size][:weight][:param=value,...]`，多个用逗号分隔

- **参数**：全局旋转或反色参数，单项参数优先

  

#### 相关配置（config.py）

- `RANDOM_VIEW_CACHE_MAX_AGE`：随机视图接口图片的 HTTP 缓存时间（秒），默认 60
- `MODULE_IMPORT_CACHE_SIZE`：随机视图模块导入缓存数量，默认 256
---

  

## 插件开发指南

  

### 1. 插件目录结构与最小实现

  

每个插件为独立目录，**最小可用插件**只需包含：

  

```

plugins/your_plugin/

├── routes.py

└── view/

└── example/

└── hm.py

```

  

- `routes.py`：注册插件视图路由（必须）。

- `view/`：视图目录，至少有一个类别（如 `example/`），类别下至少有一个尺寸（如 `hm.py`），并实现 `generate_image`。

  

**无需实现所有尺寸，未实现的接口自动返回错误提示。**

  

### 2. routes.py 模板

  

每个插件必须有 `routes.py`，内容如下（仅需改蓝图名和 PLUGIN_NAME）：

  

```python

from flask import Blueprint

import os

from modules.register.auto_view_routes import register_view_routes

  

bp = Blueprint('your_plugin_name', __name__)

PLUGIN_NAME = 'your_plugin_name'

PLUGIN_DESCRIPTION = '插件描述，可选'

  

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'view')

register_view_routes(bp, PLUGIN_NAME, VIEW_DIR)

```

  

如需 JSON 或页面接口，可参考现有插件添加注册：

  

```python

from modules.register.auto_json_routes import register_json_routes

from modules.register.auto_page_routes import register_page_routes

  

JSON_MODULE_DIR = os.path.join(os.path.dirname(__file__), 'json_module')

PAGE_DIR = os.path.join(os.path.dirname(__file__), 'pages')

register_json_routes(bp, PLUGIN_NAME, JSON_MODULE_DIR)

register_page_routes(bp, PLUGIN_NAME, PAGE_DIR)

```

  

### 3. 视图模块实现

  

每个视图（如 `view/example/hm.py`）需实现 `generate_image`：

  

```python

from .utils import prepare_canvas, finalize_image, get_font

  

def generate_image(rotate=0, invert=False, param1='默认值1'):

img, draw, font = prepare_canvas('hm', font_size=24)

# ...绘制内容...

return finalize_image(img, rotate=rotate, invert=invert)

```

  

- `rotate`/`invert` 必须保留，其他参数可自定义。

- 推荐直接复用 `view/example/utils.py` 工具函数。

  

### 4. 参数优先级与自动注册

  

- **参数优先级**：用户请求 > 插件 `plugin_config.py` > 全局 `config.py`

- 插件目录、`PLUGIN_NAME`、蓝图名建议保持一致。

- 路由自动注册，无需手动添加。

  

### 5. 推荐开发流程

  

1. 参考 `plugins/template/` 或任意现有插件结构，按需新建目录和文件。

2. 只需关注业务逻辑和视图内容，框架和注册流程无需重复实现。

3. 可只实现需要的接口和尺寸，逐步完善。

  

### 6. 工具函数与资源

  

- 推荐直接复制 `view/example/utils.py`，用于标准化画布、字体、图片处理。

- 字体、图片等资源建议放在 `assets/` 目录下，仅在代码中相对路径读取。

  

### 7. JSON 与页面接口（可选）

  

- `json_module/` 下添加 py 文件，实现 `to_json` 函数即可。

- `pages/` 下添加 html 文件，自动注册 `/your_plugin/page/页面名` 路由。
