date: 2013-08-22 08:48
title: ASP.NET MVC 3 开发过程小记（一）
permalink: aspnet-mvc-3-dev-notes-001
tags: [webdev,aspnet,mvc]
---

刚刚新建工程的时候，如果不想用 IIS Express 的话，需要自行开启配置 Windows 8 自带的 IIS 服务。在控制面板->添加删除程序左边就可以添加 IIS 服务了。

## 运行网站时出现“HTTP 错误 500.19 – 内部服务器错误”

出现这个错误时，可以先参考微软的 KB（[KB942055](http://support.microsoft.com/kb/942055)），里面很详细地介绍了9种不同的错误码下的处理方法。

如果出现 `0x80070021` 的话，可以按下面的方法处理：

先确定错误信息中提示的是 Handlers 被锁定还是 Modules 被锁定，然后开启 CMD，按需执行命令：

    %windir%\system32\inetsrv\appcmd unlock config -section:system.webServer/handlers

    %windir%\system32\inetsrv\appcmd unlock config -section:system.webServer/modules

另外，在安装 IIS 的时候，记得选中 ASP.NET，否则也会出现类似的信息。