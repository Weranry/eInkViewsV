# eInkViews
## 项目介绍
---
**eInkViews** 是一个为 [Open ePaper Link](https://openepaperlink.org) 项目中 `image_url` 功能设计的墨水屏图像信息展示服务，支持插件化扩展。它可灵活适配多种尺寸墨水屏，通过 pillow 库动态生成图片，也可直接返回对应的 Json 数据可按需调用。

eInkViews 基于 [ePapaer DashBoard](https://github.com/weranry/epaperdashboard) 升级而来，增加了插件化扩展功能，可灵活增减模块，并对图像绘制等代码进行了抽象，专注于信息与图像排版设计，解决了单片机驱动墨水屏展示大量信息的困难，以及 Open ePaper Link 不支持复杂排版和 Unicode 字符的问题。

## 快速开始
---
### 拉取仓库
```bash
git clone https://github.com/Weranry/eInkViews.git
```
### 安装依赖
```bash
pip install -r requirements.txt
```
### 安装插件
- 将第三方插件或自定义插件目录复制到 `plugins/` 文件夹下。
- 可调整插件自身目录下的 `plugin_config.py`，实现个性化设置。
### 其他配置
- 全局配置文件为 `config.py`，可进行全局配置
- 参数优先级：用户请求 > 插件 `plugin_config.py` > 全局 `config.py`
### 本地启动与调试
```bash
python test.py
```
- 启动后访问本地服务进行调试，检查插件是否正常工作
### 推送到远程仓库
```bash
git add .
git commit -m 
git push origin main
```
### 部署到 Vercel
1. 注册并登录 [Vercel](https://vercel.com)。
2. Fork 或上传本项目到你的 GitHub 仓库。
3. 在 Vercel 新建项目，选择你的仓库。
4. 保持默认设置，自动检测 `vercel.json` 配置，无需额外修改。
5. 部署完成后即可通过 Vercel 提供的域名访问服务。
6. 在 Vercel 项目设置中添加环境变量 EVKEY ，用于插件或服务鉴权。

后续如需要添加插件，可继续在`plugins/`添加并配置，重新推送到 Github 仓库后 Vercel 会自动识别并部署。

## 路由与参数
---
### 公共参数
#### 视图尺寸 Size 参数
通过设置此参数，可以调整获取到的视图大小和方向，视图适配情况视插件具体情况而定，详细可见插件文档，eInkViews预设了下列尺寸。

|参数|尺寸|方向|对应尺寸｜
|---|---|---|---|
|m|200x200|无|1.54inch|
|hL|250x122|横向|2.13inch|
|hxl|384x184|横向|3.50inch|
|h2xl|400x300|横向|4.20inch|
|h3xl|600x480|横向|5.83inch|
|h4xl|800x480|横向|7.5inch|
|vL|122x250|纵向|2.13inch|
|vxl|184x384|纵向|3.50inch|
|v2xl|300x400|纵向|4.20inch|
|v3xl|480x600|纵向|5.83inch|
|v4xl|480x800|纵向|7.5inch|

插件开发者可以通过预设的`create_custom_canvas`方法创建预设尺寸之外的大小，详细参数值可见插件文档。

#### 旋转 rotate 参数
对于返回图像，可做旋转处理，由于Open ePaperlink 的限制，当请求纵向视图时，会出现错误，所以需要对返回的图像做旋转处理。

|参数|说明|
|---|---|
|c|顺时针90°|
|cc|逆时针90°|
|h|旋转180°|
|0|默认（不旋转）|

#### 反色 invert 参数
如果对返回的图像有反转颜色的需求，可以设置此参数，但是此参数只会对黑白进行反色，而不会处理红色或者黄色，对于七色视图不起作用。

|参数|说明|
|---|---|
|t|反色|
|f|不反色|

#### 颜色模式 cmode 参数
由于墨水屏硬件的限制，可能无法使用某些插件视图的调色盘方案，需要使用此参数对图像进行对应处理，相同地，不对七色视图起作用。

|参数|说明|
|---|---|
|None|原始调色盘方案|
|2bw|将任何彩色转换为黑色|
|r2y|将红色转换为黄色|
|y2r|将黄色转换为红色|
|yr2r|将红色黄色统一为红色|
|yr2y|将红色黄色统一为黄色|


### 接口
#### Views 视图接口
eInkViews 的基础功能。
```
GET /{plugin_name}/view/{view_name}?size={size}&rotate={r}&invert={i}&param=value...
```
- **plugin_name**：插件名称
- **view_name**：插件下的视图名称
- **params**：由具体模块定义

### JSON 数据接口
可以返回 Views 使用的数据，可另作他用。
```
GET /{plugin_name}/json/{json_name}?param=value
```
- **plugin_name**：插件名称
- **json_name**：插件中的 JSON 格式名称
- **params**：由具体模块定义

### 页面接口
可用于提供插件的工具和文档。
```
GET /{plugin_name}/page/{page_name}
```
- **plugin_name**：插件名称
- **page_name**：插件中 pages/ 目录下的页面名称
- **params**：由具体模块定义

### Random Views 视图接口
可以设置多个视图的权重，实现随机展示，建议使用一致的SIZE参数。
```
GET /random/views?routes={路由描述串}&rotate={r}&invert={i}
```
- **路由描述串**：格式为 `plugin_name.view_name[:size][:weight][:param=value,...]`，多个用逗号分隔
- **参数**：全局旋转或反色参数，单项参数优先

## 插件开发
---
### 插件文件结构
插件需要满足如下结构
```
your_plugin/
├── assets/           # 插件使用的素材文件，如字体等
├── lib/              # 插件使用的业务逻辑代码
├── json_module/      # 插件以 JSON 形式返回内容的模块
├── page/             # 存储有必要的前端 HTML
├── plugin_config.py  # 插件的个性化设置
├── routes.py         # 插件的路由注册模块
└── views/            # 视图文件
  └── kind/           # 视图种类，一个插件可能存在多种视图
    └── size.py       # 具体的视图模块，绘图逻辑，如果某种类视图数量多，则应将可复用的代码封装进 utils.py 中
```
如果需要开发插件，可以复制template插件作为模板进行修改，插件的最小可用状态应该至少包含一个业务逻辑代码和视图模块。

### routes.py
每个插件必须包含一个 `routes.py` 需要设置 `your_plugin_name`和 `your_plugin_description`（可选）
```python
from flask import Blueprint
import os
from modules.register.auto_view_routes import register_view_routes
from modules.register.auto_json_routes import register_json_routes
from modules.register.auto_page_routes import register_page_routes

bp = Blueprint('your_plugin_name', __name__)
PLUGIN_NAME = 'your_plugin_name'
PLUGIN_DESCRIPTION = 'your_plugin_description'

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'view')
JSON_MODULE_DIR = os.path.join(os.path.dirname(__file__), 'json_module')
PAGE_DIR = os.path.join(os.path.dirname(__file__), 'pages')

register_view_routes(bp, PLUGIN_NAME, VIEW_DIR)
register_json_routes(bp, PLUGIN_NAME, JSON_MODULE_DIR)
register_page_routes(bp, PLUGIN_NAME, PAGE_DIR)
```
对于注册视图，JSON和PAGE的代码，如果插件没有对应功能，则可将其进行注释，但是尽量不要删除，以保证后期的可扩展性。