title: 一个在Mac上用于快速切换Function Key的Alfred Workflow
permalink: 'functionkey-swithcher-workflow'
date: 2014-06-03 13:37:51
tags: [mac,alfred,workflow]
---

最近切换到iOS开发上，每天都在忍受着Xcode和VS之间的异同。Mac上有一些比较脑残的设置（虽然有时候会觉得挺方便）。不过对开发者影响比较大的还是Debug的时候，键盘顶部的Function Keys默认被设置成了OS X上的一些快捷方式。

虽然，MAS（Mac App Store）上有一款可以自动切换Function Key的软件（叫Puala），有兴趣可以自行下载（￥6）。不过Apple提供了AppleScript，可以对OS X系统、GUI等进行编程，快速实现想要的功能。本来是想自己写一个简单的脚本做处理的，结果查阅了一下各大网站，有人已经写过了。我就简单封装成Alfred Workflow，需要的同学自行下载安装。

使用方法：呼出Alfred之后，输入swfn回车即可将按钮功能切换成标准的Function Key。

[点击下载](https://www.dropbox.com/s/ptdtvpsoa1gwzm2/Switch%20FunctionKeys.alfredworkflow)。