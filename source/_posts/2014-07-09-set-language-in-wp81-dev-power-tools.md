title: 为Windows Phone Developer Power Tools设置语言
permalink: set-language-in-wp8.1-dev-power-tools
date: 2014-07-09 10:15:51
tags: wp
---

WP8.1 SDK新添加了一个工具叫做[Developer Power Tools](http://msdn.microsoft.com/zh-cn/library/windows/apps/dn629255.aspx)，这个工具比以前的Profile工具好用（虽然还是不会用，找内存泄漏太难了）。本文主要是为了解决一个问题：__在中文系统上安装英文的VS2013后，启动Power Tools发现连接的模拟器名字多了一个“zh-HANS”，导致Debug的模拟器和Power Tools启动的模拟器不是同一个的问题__。

废话少说，直接上干货。

设置Power Tools的启动语言，只需要在对应快捷方式的目标路径中添加`-language en-US`即可，例如：

    "C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.1\Tools\PowerTools\PwTools.exe" -language en-US

有空补个截图吧。

PS：MSDN文档能不能完善一点，新加一个新工具竟然连使用说明都没有。ETL文件怎么分析也没说，哎。这启动参数还是用JustDecompile反编译出来才发现的。调了半天以为格式是"-language=en-US"，再仔细看才发现是用空格区分的。

PSS：参数用/或者-开头都可以。

