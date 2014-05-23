date: 2013-08-28 21:55
title: 解决 IE11 无法代理到 Fiddler 进行抓包
permalink: local-proxy-and-ie-enhanced-protected-mode
tags: [webdev,fiddler]
---

# 解决 IE11 无法代理到 Fiddler 进行抓包

这个问题很诡异，今天尝试更新到 Windows 8.1 RTM 之后，发现开启 Fiddler 后无法对 IE 进行抓包，具体情况如下：

1. 开启 Fiddler，设置本地代理和出口网关
2. 在 Chrome 中可以正常抓包，但在 IE 中尝试打开网页时 Fiddler 中没有观察到有任何流量
3. 运行 Fiddler Tools > Sandbox 选项，网页可以正常打开，但仅限运行过此选项的 IE 实例，关闭网页重新打开，IE 仍然无法正常使用。

这个问题确实让人很恼火，很神奇的问题。最后是怎么解决的呢？在乱打乱撞之下，在 **Internet 选项 -> 高级 **选项页中，把**增强的保护模式**给关闭之后，Fiddler 又可以正常捕捉到 IE 的流量了。

后来查了一下 Google，发现有人在使用 GoAgent 的时候也出现过这样的情况。总的来说，就是这个**增强的保护模式**惹的祸。