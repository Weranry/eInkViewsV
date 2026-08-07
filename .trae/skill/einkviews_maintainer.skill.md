---
name: "eInkViews Maintainer Skill"
user-invocable: true
description: "Work-flow skill for maintaining the eInkViews core framework, deployment compatibility, and shared infrastructure."
---

# eInkViews 维护 Skill

## 适用场景

- 修改 `modules/`
- 修改 `config.py`
- 修改 `app.py`、`test.py`
- 修改 `vercel.json`
- 调整 `requirements.txt`
- 修复共享基础设施或部署兼容问题

## 强制规则

- 只处理框架层，不进入 `plugins/` 做插件开发
- 保持 Vercel Serverless 兼容：无状态、无本地临时文件、无长驻进程
- 不使用 `app.logger.exception()`
- 所有 Python 命令必须带 `-B`
- 禁止创建或激活虚拟环境
- 禁止引入未声明依赖
- 路径必须使用 `os.path.join(os.path.dirname(__file__), ...)`
- 测试只能用 `python -B test.py`

## 推荐工作流

1. 先定位控制行为的核心模块
2. 只做最小必要改动
3. 修改后立刻做局部验证
4. 如果涉及路由或配置，检查全局优先级是否仍正确
5. 如有破坏性风险，先说明再改

## 核心原则

- 参数优先级保持为：URL > 插件默认值 > 全局默认值
- 公共 API 优先向后兼容
- 日志、异常、路径、依赖都要符合部署限制
- 不要为了局部问题扩大重构范围

## 常见任务

- 错误处理：保持统一 JSON 错误格式
- 画布工厂：保证尺寸和调色板兼容
- 字体加载：保持根字体与插件字体逻辑清晰
- 路由注册：与 Flask / Vercel 路由一致
- 随机路由：参数解析和权重选择保持稳定

## 验证方式

- 首选 `python -B test.py`
- 必要时再做针对性检查
- 不用 `app.py` 启动测试
