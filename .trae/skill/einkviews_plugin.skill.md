---
name: "eInkViews Plugin Skill"
user-invocable: true
description: "Work-flow skill for creating, modifying, or debugging eInkViews plugins under plugins/."
---

# eInkViews 插件 Skill

## 适用场景

- 新建插件
- 修改插件视图
- 修复插件数据抓取或参数问题
- 调整 `README.md`、`plugin_config.py`、`routes.py`

## 强制规则

- 每次改插件逻辑，都要同步更新插件自己的 `README.md`
- 视图层只负责渲染，不负责参数兜底或默认值补全
- 先拿数据，再创建画布
- 黑色必须显式用 `fill=1` 或 `fill=(0,0,0)`
- 所有网络请求必须设置 `timeout`
- 文本尺寸必须用 `draw.textbbox()` 计算
- 位图必须做 Floyd-Steinberg 抖动
- 默认同时实现 `hxl` 和 `h2xl`
- `h2xl` 必须独立布局，不得简单缩放
- 测试入口只能用 `python -B test.py`

## 推荐工作流

1. 确认插件类型和必要参数
2. 先写 `lib/`，把数据和校验处理好
3. 再写 `view/<kind>/hxl.py` 和 `view/<kind>/h2xl.py`
4. 把可复用的绘图逻辑放进 `view/<kind>/utils.py`
5. 更新插件 `README.md`
6. 用完整测试 URL 验证结果

## 目录要求

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

## 参数处理

- URL 参数优先级最高
- 插件默认值放在 `plugin_config.py`
- 全局兜底值放在 `config.py`
- 地理位置类只在需要时校验 `lat` / `lon` / `tz`
- 用户标识类校验 `username`
- 资源文件类缺文件直接抛 `NotFoundError`

## 视图写法

- 只做布局，不做业务判断
- 标题、主数值、说明文字分层清楚
- 元素绘制前先检查右边界和下边界
- 优先使用项目根字体；私有字体只在文件真实存在时使用
- 红色用于强调，不要堆满整张图

## 测试链接模板

- 地理位置类：`http://127.0.0.1:5000/openmeteo/view/now?size=hxl&lat=31.23&lon=121.47&tz=Asia/Shanghai`
- 用户标识类：`http://127.0.0.1:5000/github/view/dashboard?size=hxl&username=octocat`
- 内容选择类：`http://127.0.0.1:5000/hitokoto/view/quote?size=hxl`
- 资源文件类：`http://127.0.0.1:5000/schedule/view/schedule_view?size=hxl`
- 纯内容类：`http://127.0.0.1:5000/zhihu/view/daily?size=hxl`

## 交付检查

- [ ] `routes.py`、`plugin_config.py`、`README.md` 已同步
- [ ] `hxl` 和 `h2xl` 都能独立生成
- [ ] 没有把 `palette` 写进测试 URL
- [ ] 没有在视图层做参数降级
- [ ] 没有遗漏边界检查
