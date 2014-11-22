title: 编译wxSQLite3 for WinRT
permalink: compile-a-wxsqlite3-for-winrt
date: 2014-11-22 22:52:55
tags: [winrt,sqlite] 
---

原生的SQLite没有实现加解密接口，只留了一个函数入口给开发者自行实现。在Windows下面本身提供了一个跟ADO.NET紧密结合的SQLite，支持加解密。但WinRT上面使用的还是原生的SQLite，这就只能依靠开发者自己去实现一个加解密流程。幸好wxWidget这开源工程里面本来就实现了一个支持AES 128/256位加密的SQLite，只需要将这个wxSQLite按照WinRT的编译流程去编译打包成VSIX包就可以了。具体的实现，我已经把[已编译的包和可编译的源码都放在Github上](https://github.com/blastmann/wxSqlite3-WinRT-Project)了，有兴趣的可以去弄一下。

注意点：

1. 编译前需要安装好Cygwin、Active Tcl 8.5和zip\unzip命令。
2. 原版的SQLite-Net没有导入和封装加解密函数，同样的在源码里面已经有封装好的了。
3. 个人只测试了加解密和数据库读取能正常工作，不确保在写入的时候会有异常情况发生，欢迎在repo里面留下issue。