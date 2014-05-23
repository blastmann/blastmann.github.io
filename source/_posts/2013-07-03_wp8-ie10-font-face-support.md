date: 2013-07-03 17:19
title: WP8 上的 IE10 对 @font-face 属性的支持程度
permalink: wp8-ie10-font-face-support
tags: [webdev,wp8]
---


现在的前端都流行把一些小图标转换成字体，然后利用 `@font-face` 这个 CSS 属性来定义一个页面专有的字体，从而达到把小图标转换成字符显示的效果。这样做除了可以省流量，图标的显示效果也很好，放大缩小都不怎么会影响效果，确实是一个不错的的手段。

关于 CSS3 中的 `@font-face` 属性，可以参阅[这篇文章](http://www.w3cplus.com/content/css3-font-face)，里面有很详细的属性应用介绍。

但是，在 PC 的 IE10 下面尝试嵌入 ttf 格式的字体时，会提示这样的信息：

> CSS3114: @font-face 未能完成 OpenType 嵌入权限检查。权限必须是可安装的。 

原因可能是自制的 ttf 格式没有正确的安装权限造成的。因此，有必要对 ttf 格式进行转换，PC 上的 IE10 支持多种字体格式，如 Embedded-Opentype(eot)、Web Open Font Format(woff)、TrueType(ttf) 和 Scalable Vector Graphics(SVG)，具体可以参考上面文章。

但 WP8 上的 IE10 对字体格式的要求更严格，转换成 IE 专用的 eot 格式之后还是不能正常显示。于是又查了一下资料，发现还是能用的（[点击这里](http://stackoverflow.com/questions/15819717/font-awesome-not-displayed-on-windows-phone-8)）。于是把格式换成 woff 之后就没有问题了，ttf 转 woff 的工具在网上都有，可以在线转换（[点击这里有一个网站可以试试](http://everythingfonts.com/)）。

PS：最好还是在引用的 url 后面声明一下字体的格式。

    @font-face {
        font-family: 'Test';
        src:url(font/font.woff) format('woff');
    }
