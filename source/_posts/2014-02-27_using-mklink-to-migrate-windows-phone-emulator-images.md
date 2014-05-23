date: 2014-02-27 11:47
title: 使用mklink迁移Windows Phone SDK的模拟器镜像
permalink: using-mklink-to-migrate-windows-phone-emulator-images
tags: wp8
---

自从Windows 7引入mklink命令后，再也不用担心系统盘的空间不足了。本来我个人对所有要安装的软件的态度都是放在系统盘里面的，毕竟系统重装之后软件基本都要重装，而且即使安装的时候使用别的盘，安装程序仍然会把部分数据放到系统盘内。但是后来却出现了开发环境占用硬盘空间太多的问题（还是因为系统分区分得太小了），于是开始把部分开发环境的数据迁移到另外的分区里面。

模拟器镜像的位置在`C:\Program Files (x86)\Microsoft SDKs\Windows Phone`，主要占空间的几个大头都是v8.x里面的Emulator目录。迁移的时候只需把目录剪切到别的分区中，然后运行下面的命令建立对应目录的符号链接即可。由于GDR2和GDR3目录下面都只存放了模拟器镜像，所以下面的命令中是直接对这两个目录进行符号链接。

示例（请使用管理员权限运行）：

    mklink /D "C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0\Emulator" "D:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0\Emulator"
    mklink /D "C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0GDR2" "D:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0GDR2"
    mklink /D "C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0GDR3" "D:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.0GDR3"
    mklink /D "C:\Users\xxx\AppData\Local\Microsoft\XDE" "D:\AppData\Local\Microsoft\XDE"

相关资料：

1. [关于mklink命令](http://technet.microsoft.com/zh-cn/library/cc753194(v=ws.10).aspx)
2. [关于符号链接](http://technet.microsoft.com/zh-cn/library/cc754077(v=WS.10).aspx)