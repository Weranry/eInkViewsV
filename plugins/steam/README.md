# Steam 统计插件

提供 Steam 玩家信息的视图接口，自动适配多尺寸网格（Grid）布局。

## API 接口

### 视图 (View)
- `GET /steam/view/stats?size=<size_key>&api_key=<your_api_key>&steam_id=<your_steam_id>`
    - 获取玩家最近游玩、总时长、等级、昵称等信息的图片
    - `api_key`: 必选，Steam Web API Key
    - `steam_id`: 必选，Steam ID (64位)
    - `size_key`: 支持 `hxl`, `h2xl`, `v2xl`（3.5寸, 4.2寸 和竖屏 4.2寸），后台采用通用 Grid 布局引擎自适应支持更多尺寸。

## 示例
- 横屏 3.5 寸: [http://127.0.0.1:5000/steam/view/stats?size=hxl&api_key=SET_KEY&steam_id=SET_ID](http://127.0.0.1:5000/steam/view/stats?size=hxl&api_key=SET_KEY&steam_id=SET_ID)
- 横屏 4.2 寸: [http://127.0.0.1:5000/steam/view/stats?size=h2xl&api_key=SET_KEY&steam_id=SET_ID](http://127.0.0.1:5000/steam/view/stats?size=h2xl&api_key=SET_KEY&steam_id=SET_ID)
- 竖屏 4.2 寸: [http://127.0.0.1:5000/steam/view/stats?size=v2xl&api_key=SET_KEY&steam_id=SET_ID](http://127.0.0.1:5000/steam/view/stats?size=v2xl&api_key=SET_KEY&steam_id=SET_ID)
