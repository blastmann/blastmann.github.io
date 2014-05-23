date: 2013-08-29 11:20
title: IE11 兼容性小指南
permalink: ie11-compatibility-guide
tags: [webdev,css3,ie]
---

手贱升级了 Windows 8.1 之后，发现 IE11 在 HTML5 兼容性又有变化，感觉十分蛋疼，写篇文章记录一下遇到的两个比较明显的问题。

关于“增强的保护模式”和代理问题，大家可以看一下[这篇文章](http://blog.edi-c.com/post/local-proxy-and-ie-enhanced-protected-mode)。

## 文档模式的变化

[![ie11-dev-tool](http://d.pr/i/tbnI.png)](http://d.pr/i/tbnI)

IE11 中默认使用两种文档模式：IE7 和 Edge。IE7 的文档模式跟兼容模式类似，而 Edge 模式则是指当前版本的 IE 下可以使用的最高的文档模式。IE 开发者工具中只能选这两种模式，如果要使用指定的文档模式（如 IE10 或者 IE9），则需要在页面中添加指定的 `meta` 标签，如下（按需选择添加）：

    <meta http-equiv="x-ua-compatible" content="IE=10" >
    <meta http-equiv="x-ua-compatible" content="IE=9" >
    <meta http-equiv="x-ua-compatible" content="IE=8" >
    <meta http-equiv="x-ua-compatible" content="IE=7" >

如果需要测试 Quirks Mode，则可以使用下面的标签之一：

    <meta http-equiv="x-ua-compatible" content="IE=EmulateIE9" >
    <meta http-equiv="x-ua-compatible" content="IE=EmulateIE8" >
    <meta http-equiv="x-ua-compatible" content="IE=EmulateIE7" >

## Flexbox（弹性框）布局更新

需要更详细的信息的话，可以到[这篇文章](http://msdn.microsoft.com/zh-cn/library/ie/dn265027(v=vs.85).aspx)进行查阅。

IE11 里面，Flexbox 的更新主要是一些属性名字的变化（表现也有少量变化，考虑到这本来就属于测试性的属性，变化也是正常）。下面根据官网的更新内容简单总结一下：

下面的属性命名在 IE11 中发生了变化：

  IE10  |  IE11
------- | -------
`-ms-flex-wrap` | `flex-wrap`
`-ms-flex-order`  和 `flex-order` | `order`
`-ms-flex-pack` | `justify-content`
`-ms-flex-align` | `align-items`
`-ms-flex-item-align` | `align-self`
`-ms-flex-line-pack` | `align-content`

下面的属性所支持的值也发生了变化：

Property | Old value | New value
-------- | --------- | ---------
`display` | `-ms-flexbox` | `flex`
`display` | `-ms-inline-flexbox` | `inline-flex`
`flex-wrap` | `none` | `nowrap`
`align-content`/`align-items`/`align-self`/`justify-content` | `start` | `flex-start`
`align-content`/`align-items`/`align-self`/`justify-content` | `end` | `flex-end`

当然，部分旧的值仍然有效（如`display:-ms-flexbox`），但是部分属性变化将有变化，如下面所说的 `flex` 属性。

### flex 属性

官方文档中作了以下的注明：

* 已添加 `flex` 属性，作为 `flex-grow`、`flex-shrink` 和 `flex-basis` 属性的速记属性。
* `align-content` 和 `justify-content` 属性现在支持值 `space-around` 与 `space-between`。
* 弹性项目的默认弹性行为已更改。 在 Internet Explorer 10 中，不适合容器的弹性项目将溢出容器边缘或者是被修剪到与容器边缘对齐。 现在，从 IE11 Preview 开始，这些项目将缩小来适应其容器（如果指定，则最小缩至 `min-width` 值）。 使用 `flex-shrink` 属性可更改此行为。

让人蛋疼的是第三点（虽然现在看起来可以理解），下面有个 demo 可以让大家理解一下。

    IE10下：
    <style>
        .container{
            width: 400px;
            height: 200px;
            overflow: hidden;
        }

        #msflexbox{
            display: -ms-flexbox;
        }

        .dodgerBlue{
            background: dodgerBlue;
            width: 100%;
        }

        .limeGreen{
            background: limeGreen;
            width: 100%;
        }
    </style>

效果图：

[![ie10-flexbox-overflow](http://d.pr/i/g518.png)](http://d.pr/i/g518)

此时 `container` 中的元素将会充满整个 `container`，溢出的部分则被 `overflow:hidden` 所隐藏（淡蓝色部分为 Inspector 高亮）。

而同样的 CSS 在 IE11 下将会表现如下图：

[![ie11-flexbox-shrink](http://d.pr/i/aOMl.png)](http://d.pr/i/aOMl)

这样则会造成一定的适配问题，如果需要在 IE11 下展示与 IE10 相同的效果，则可以调节 `flex-shrink` 此属性（[相关文档](http://msdn.microsoft.com/en-us/library/ie/dn254948(v=vs.85).aspx)）。我们对 `.container` 下的元素添加一个 CSS `flex-shrink: 0;`，则两个版本的表现一致。

关于 Flexbox 的布局，我将在[另外的一篇文章](http://blog.edi-c.com/post/flexbox-layout)中进行叙述。