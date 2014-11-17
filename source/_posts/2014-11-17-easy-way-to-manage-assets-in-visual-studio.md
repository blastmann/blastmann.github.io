title: 利用Link大法让Visual Studio工程文件自动更新Assets
permalink: 'easy-way-to-manage-assets-in-visual-studio'
date: 2014-11-17 19:50:46
tags: [winrt,vs2013]
---

前段时间在做[MH4 Dex RT](http://www.windowsphone.com/s?appid=fb0ce559-ea2a-4447-abac-599da5e90e50)的时候，Ping叔给了一堆图片资源，都是一些小图标。每次做完图片处理之后都要重新拉到工程里面，做了好几次的时候就觉得超麻烦。每次往VS里面拖图片都会被它自动复制一份，拖的时候还会卡住一段时间。想了半天要不要用脚本解决这问题，最后发现我大VS竟然提供了一个特别的功能叫"Add as Link"。简单修改一下工程文件就可以让VS自动更新工程目录下的工程资源了。

