date: 2013-05-14 12:35
title: Fiddler 与 Windows Phone 联调
permalink: fiddler_share
tags: [webdev,fiddler,notes]
---

最近对浏览器的页面显示进行调节的时候，不得不使用 [Fiddler][fiddler] 进行本地代理调试。下面简单对使用进行介绍，主要是参考[**这个链接**][tutorial]。

#### 使用 Fiddler 对 WP8 模拟器进行抓包

首先我们先去 Fiddler 官方网站下载一个最新的版本（[点击下载][fhome]）。由于 Windows Phone 8 的模拟器是以 Hyper-V 虚拟机的形式运行，所以它在网络中相当于一台独立的设备。我们需要对 Fiddler 进行监控远程设备的设置。

1.  安装启动 Fiddler
2.  按照下面的顺序开启菜单：`Tools` > `Fiddler Options` > `Connections`
3.  选中 `Allow remote computers to connect`，确定设置

    ![remote connection](http://d.pr/i/6mqR.png)

4.  返回主界面，在界面右下角有一个黑色的区域，称为 `QuickExec Box`，在输入框中输入下面的命令，其中 `IP Address` 为你本机的 IP 地址（设置为本机的主机名亦可）：

        prefs set fiddler.network.proxy.registrationhostname [IP Address]

    ![QuickExec](http://d.pr/i/1WTT.png)

5.  设置完成后，重新启动 Fiddler 和模拟器，用模拟器中的浏览器打开页面，看能否正常抓包。PS：除了模拟器的流量，本地流量也会同时显示在 Fiddler 中。

#### 使用 Fiddler 对 WP8 设备进行抓包

基本设置与上面的步骤是一样的，我们只需要对设备的 WiFi 接入点进行一点设置即可。

1. 打开设备中的 `设置` > `WiFi`
2. 选择你已经连接的 WiFi 接入点，进入高级设置
3. 高级设置中启用代理服务器，服务器地址为你本机的 IP 地址，端口是8888。
4. 设置完成后手机将通过 PC 代理进行联网，此时即可在 Fiddler 中对其抓包处理。

#### 利用 Fiddler 本地调试网页资源

这部分就比较简单了，属于 Fiddler 的一个最常用的功能。

1. 在列表中选择一项抓包内容，打开右键菜单选择将该内容保存到本地
2. 选择右边的 AutoResponder，勾选 `Enable automatic responses` 和 `Unmatched requests passthrough`
3. 点击 `Add` 添加规则
4. 在下面列表中选择本地保存下来的文件，然后点击 `Save`
5. 此时可以尝试修改本地的文件内容，测试是否代理成功。


[fiddler]: http://fiddler2.com/home
[tutorial]: http://www.spikie.be/blog/post/2013/01/04/Windows-Phone-8-and-Fiddler.aspx
[fhome]: http://fiddler2.com/get-fiddler