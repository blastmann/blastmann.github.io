date: 2013-06-14 13:53
title: 在 Windows Phone 上利用 weinre 远程调试 HTML5 页面
permalink: remote-html5-debugging-on-windows-phone-with-weinre
tags: [webdev,wp8]
---

参考资料：

* [Remote HTML5 debugging on Windows Phone with weinre](http://blogs.windows.com/windows_phone/b/wpdev/archive/2013/06/12/remote-html5-debugging-on-windows-phone-with-weinre.aspx)
* [Now on IE and Firefox: Debug your mobile HTML5 page remotely with weinre (WEb INspector REmote)](http://msopentech.com/blog/2013/05/31/now-on-ie-and-firefox-debug-your-mobile-html5-page-remotely-with-weinre-web-inspector-remote/)
* [How to debug Windows Phone HTML5 Apps](http://www.developer.nokia.com/Community/Wiki/How_to_debug_Windows_Phone_HTML5_Apps)

## weinre (WEb INspector REmote)

Weinre (WEb INspector REmote) 是一个用于调试 HTML5 页面在移动设备上表现的工具。它是 Apache Cordova 计划中的一部分，旨在帮助开发者在设备上远程调试他们的网页或那些基于 Cordova 的移动 App。 Weinre 可远程地进行 DOM 的审查，让开发者在设备上调试 HTML5 页面显示效果更为方便。

如果你熟悉 IE 上的 F12 审查工具、Firefox 上的 Firebug 或 Chrome 的 Web 审查工具，那你将会十分熟悉 Weinre，因为它们非常相像。

## 安装部署

1.  到 [Node.js](http://nodejs.org/) 对应平台的版本，安装部署 Node.js。
2.  启动 Node.js 的命令提示符，输入下面命令安装 weinre：`npm -g -install weinre`

    *PS*：如系统有设置代理的话，可在环境变量中添加 `http_proxy` 和 `https_proxy` 两个变量，并设置为代理地址。

3.  安装完成后，输入以下命令启动 weinre： `weinre -boundHost xx.xx.xx.xx`，`xx.xx.xx.xx` 你想要绑定的网络适配器 IP 地址。
4.  在浏览器中输入 `http://xx.xx.xx.xx:8080` 即可打开 weinre 页面。页面如下：

    ![weinre_console](http://d.pr/i/qRTc.png)

## 开始调试

如果你所在的网络环境不复杂的话，其实已经可以开始调试你的页面了。步骤如下：

1.  在 PC 上启动调试器客户端页面：http://xx.xx.xx.xx:8080/client（xx.xx.xx.xx 的含义如上文所述），打开后可以看到下面的界面：

    ![weinre_client](http://d.pr/i/AvaR.png)

2.  在需要调试的页面中加入下面的标签：

        <script src=”http://xx.xx.xx.xx:8080/target/target-script-min.js#anonymous”></script>

3.  然后在应用中打开需要调试的页面，即可在开始调试。

*PS*：关于如何使用 Fiddler 与 Windows Phone 进行联合调试，可以参考这篇文章：《[Fiddler 与 Windows Phone 联调](http://scriptogr.am/blastmann/post/fiddlershare)》。
