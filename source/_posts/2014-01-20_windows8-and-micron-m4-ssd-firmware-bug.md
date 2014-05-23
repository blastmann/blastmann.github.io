date: 2014-01-20 15:20
title: Windows 8.1与镁光M4 SSD固件Bug
permalink: windows8-and-micron-m4-ssd-firmware-bug
tags: system
---

最近家里的机器经常出现休眠之后无法开机的问题，刚开始的时候以为BIOS里面设置有问题，重置了一下发现还是会出现类似的问题。于是开始怀疑是不是硬盘的问题，然后想起上次刷SSD固件时候已经大半年之前了。查了一下镁光官网的固件更新，发现M4的固件又更新了好几次。最近一次更新说明里面有这么一段：

> 该固件解决了一个电源时序问题，该问题可能会导致电脑从休眠会睡眠状态唤醒时引起固态硬盘挂起，导致无法与主机进行通信（丢盘现象）。

于是去[镁光官网查找一下新的固件](http://www.crucial.com/support/firmware.aspx)，下载更新程序之后在Windows下直接更新即可。

PS：但是更新程序在更新过程里面有可能提示更新失败，然后重启之后却发现固件版本号变了。只能当作更新成功了吧~

更新完固件之后还以为Bug已经修复了，结果后面又出现了两次死机，关机之后系统就出问题了。本来想重装系统，但手上又没有完整的安装盘，于是只能跑一下`sfc`尝试修复。相关链接：[使用系统文件检查器工具修复丢失或损坏的系统文件](http://support.microsoft.com/kb/929833)。

在运行`sfc /scannow`之后，提示`urlmon.dll`无法修复（有的时候需要打开C:\Windows\Logs\CBS\CBS.log，搜索文件中记录文件无法修复的日志项，查出损坏的文件）。在Windows 8.1下面，如果这个文件损坏了，系统里面很多程序都会出现无法启动的情况，像IE、搜索、Metro系统设置等。按照文章里面的修复方法，关键的三个命令是：

* 取得损坏系统文件的管理权：`takeown /f Path_And_File_Name`
* 授予管理员对已损坏系统文件的完全访问权限：`icacls Path_And_File_Name /GRANT ADMINISTRATORS:F`
* 将损坏的系统文件替换为已知完好的文件副本：`Copy Source_File Destination`

远程控制之后终于修复了，在此记录一下。