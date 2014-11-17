title: 利用Link大法让Visual Studio工程文件自动更新Assets
permalink: 'easy-way-to-manage-assets-in-visual-studio'
date: 2014-11-17 19:50:46
tags: [winrt,vs2013]
---

前段时间在做[MH4 Dex RT](http://www.windowsphone.com/s?appid=fb0ce559-ea2a-4447-abac-599da5e90e50)的时候，Ping叔给了一堆图片资源（几千张），都是一些小图标。每次做完图片处理之后都要重新拉到工程里面，做了好几次的时候就觉得超麻烦。每次往VS里面拖图片都会被它自动复制一份，拖的时候VS还会卡住好长一段时间。想了半天要不要用脚本解决这问题，最后发现我大VS竟然提供了一个特别的功能叫"Add as Link"。简单修改一下工程文件就可以让VS自动更新工程目录下的工程资源了。

以Universal Project为例，用编辑器打开.Shared目录下面的`.projitems`文件，进行下面的操作：

1. 找到原来的Assets目录声明，一般在某个ItemGroup里面。
2. 用下面的XML片段替换：

        <Content Include="$(MSBuildThisFileDirectory)Assets\**\*.*">
            <Link>Assets\%(RecursiveDir)%(FileName)%(Extension)</Link>
        </Content>

3. 保存，在VS里面重新加载工程。

如此修改之后，以后在Shared工程里面添加资源后，只要在VS里面进行一次Project Reload即可更新Assets，十分方便快捷。

PS：此方法也适用于一份代码共享多个工程的情况。

PPS：不要尝试在VS里面对Link的资源进行复制、删除等操作。