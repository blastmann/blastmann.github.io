date: 2014-08-04 22:10
title: 让WinRT 8.1 Webview支持任意站点下的JS通知
permalink: a-solution-for-any-hosts-to-notify-winrt-8.1-webview
tags: [winrt,webview]
---

## 前言

在使用WebBrowser\Webview一类的控件时，一般都免不了与JS打交道。从WP7开始，微软的WebBrowser就支持使用`ScriptNotify()`进行JS与C#代码间的交互，到WinRT下面仍然有这么一个API供开发者使用，但适用情况有些许改变。

## 问题描述

WinRT 8.1下，微软增强了Webview控件的大部分功能，同时也废弃了几个允许脚本通知（ScriptNotify)的属性。关于ScriptNotify，在8.1的帮助文档里面有这么一段注释：

> To enable an external web page to fire the ScriptNotify event when calling window.external.notify, you must include the page's URI in the ApplicationContentUriRules section of the app manifest. (You can do this in Visual Studio on the Content URIs tab of the Package.appxmanifest designer.) The URIs in this list must use HTTPS and may contain subdomain wildcards (for example, "https://*.microsoft.com"), but they can't contain domain wildcards (for example, "https://*.com" and "https://*.*"). The manifest requirement does not apply to content that originates from the app package, uses an ms-local-stream:// URI, or is loaded using NavigateToString.
Note  If you have more then one subdomain, you must use one wildcard for each subdomain. For example, "https://*.microsoft.com" matches with "https://any.microsoft.com" but not with "https://this.any.microsoft.com."
These changes do not affect apps compiled for Windows 8, even when running on Windows 8.1.

> AllowedScriptNotifyUris, AnyScriptNotifyUri, and AllowedScriptNotifyUrisProperty are not supported in apps compiled for Windows 8.1.

也就是说，只有在应用开发过程中，开发者主动添加在`Package.appxmanifest`中的，并且只能是HTTPS下的Uri才可以进行脚本的主动通知。开发者无法直接地对非HTTPS的站点进行JS注入后的主动通知，而且需要维护一个庞大的白名单。

## 解决思路：微软的示例代码中有一段神奇的注释

在微软给出的Webview示例中，有这么一段注释：

> Content loaded using the NavigateToString() method; or ms-appx-web, ms-appdata, ms-webview-stream:// URI schemes can get the result back automatically. 

有两种情况，Webview可以无视上面描述的通知限制。

1. 使用`NavigateToString()`显示的页面
2. 使用`ms-appx-web`、`ms-appdata`和`ms-webview-stream://`导航显示的页面

那么，这个问题就转变成：能否在其它网站页面中引入一个本地页面作为与本地C#代码进行交互呢？

答案是可以的。

经过测试，我们完全可以在应用中引入一个HTML文档，文档中只需要简单地在页面中封装`window.external.notify()`这个JS函数。然后在任意页面中通过JS创建`iframe`标签并使用`ms-appx-web`协议引用这个本地的HTML文档。只要HTML文档可以正常加载，那么问题将转化为：如何对`iframe`进行跨域通信？

关于`iframe`的跨域通信，网上有不少的解决方法。在我的示例中只使用了`postMessage`这个HTML5 API进行通信（不兼容IE8以下）。

![any-uri-notify](https://xbyjdw.bn1.livefilestore.com/y2pB5LW1JARe7w32dZ04XD6eijpeYMoYH9g8tKZKnIoJib-7W5OVK8B5ypBVHG6A0zjIMoYqIanjg6fBOXg86IIro4UTz_isP0gsXvEaF_L9C4/any-uri-notify.png?psid=1)

示例代码下载：[点击下载](https://www.dropbox.com/s/tv2sq7qt9ybuopz/Control_WebView.zip)。

PS：微软限制JS的通知当然是出于安全性的考虑了，所以我们在使用这种方法的时候，也需要好好考虑一下会不会造成什么安全隐患。另外，我个人是希望JS通知这东西能少则少，毕竟性能也不是很好，建议尽量是减少使用的。