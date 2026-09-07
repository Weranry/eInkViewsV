# 知乎日报插件

提供知乎日报的视图接口。

## API 接口

### 视图 (View)
- `GET /zhihu/view/daily?size=<size_key>`
    - 获取当前知乎日报的图片
    - `size_key`: 支持 `h2xl` 等

## 示例
- [http://127.0.0.1:5000/zhihu/view/daily?size=h2xl](http://127.0.0.1:5000/zhihu/view/daily?size=h2xl)
