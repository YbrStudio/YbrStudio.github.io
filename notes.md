# mkdocs使用备忘录
## Bilibili视频嵌入模板
```html
<div style="position: relative; padding: 30% 45%;">
<iframe style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;" src="https://player.bilibili.com/player.html?cid=145147963&aid=84267566&page=1&as_wide=1&high_quality=1&danmaku=0" frameborder="no" scrolling="no"></iframe>
</div>
```

来源:https://www.cnblogs.com/wkfvawl/p/12268980.html
感谢原作者

| 参数 | 说明 |
| --- | --- |
| aid | 视频ID 就是B站的 avxxxx 后面的数字 |
| cid | 应该是客户端id, clientId 的缩写(.predicted, not accurate) 经过测试, 这个字段不填也有用 |
| page | 第几个视频, 起始下标为 1 (默认值也是为1) 就是B站视频, 选集里的, 第几个视频 |
| as_wide | 是否宽屏 1: 宽屏, 0: 小屏 |
| high_quality | 是否高清 1: 高清, 0: 最低视频质量(默认) 如视频有 360p 720p 1080p 三种, 默认或者 high_quality=0 是最低 360p high_quality=1 是最高1080p |
| danmaku | 是否开启弹幕 1: 开启(默认), 0: 关闭 |



## 内置Icon查找
https://squidfunk.github.io/mkdocs-material/reference/



## 网格模板
https://squidfunk.github.io/mkdocs-material/reference/grids/

```html
<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mkdocs-material`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Getting started](#)

-   :fontawesome-brands-markdown:{ .lg .middle } __It's just Markdown__

    ---

    Focus on your content and generate a responsive and searchable static site

    [:octicons-arrow-right-24: Reference](#)

-   :material-format-font:{ .lg .middle } __Made to measure__

    ---

    Change the colors, fonts, language, icons, logo and more with a few lines

    [:octicons-arrow-right-24: Customization](#)

-   :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    Material for MkDocs is licensed under MIT and available on [GitHub]

    [:octicons-arrow-right-24: License](#)

</div>
```

```html
<div class="grid cards" markdown>

- :fontawesome-brands-html5: __HTML__ for content and structure
- :fontawesome-brands-js: __JavaScript__ for interactivity
- :fontawesome-brands-css3: __CSS__ for text running out of boxes
- :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

</div>
```

```html
<div class="grid" markdown>

:fontawesome-brands-html5: __HTML__ for content and structure
{ .card }

:fontawesome-brands-js: __JavaScript__ for interactivity
{ .card }

:fontawesome-brands-css3: __CSS__ for text running out of boxes
{ .card }

> :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

</div>
```