date: 2012-12-26 12:12
title: Sublime Text中的任务管理
permalink: task-management-in-st2
tags: st2
---

## 说在前面
个人用过很多任务管理软件，虽然觉得像[Producteev]()、[Evernote]()之类的都可以比较方便地做一下任务管理，但是总是觉得没有一个软件可以很方便地集成我所想的功能。我希望可以在一个地方添加完成任务之后，在同一个地方执行任务，例如写一下Markdown什么的，这样我有时就不怎么想分开两个工作的地方了，可以在一个地方里面完成我的工作感觉还是挺方便的，于是当我看到PlainTask这插件之后就觉得这东西太有趣了，正好它也有个OmniFocus的主题，随便可以拿来用一下。

有的时候一个适合自己的GTD系统还是挺重要的，如果觉得自己没什么资金去买一个OmniFocus这样贵的软件（iOS上是一百多，Mac上的是三百多），而且OmniFocus这东西还不是跨平台的，如果要跨越Mac\iOS\Windows的话就只能用Producteev、Evernote、Doit.im等软件，那些都用得不是很顺。个人的工作环境中比较多的时间还是集中在PC前面，而且有时候也不希望多打开一个别的软件影响自己的工作，于是就觉得PlainTask这东西很适合我平常的工作。因为我平常也有很长时间需要打开Sublime Text这东西，在不影响自己的工作窗口切换的前提下可以使用这东西完成很多事情。这样的感觉很好，同时Sublime Text里面还可以集成Git，我再把文件夹放到网盘上，刚好可以做成一个的版本控制的GTD管理系统。虽然暂时只适用于PC之间的切换，并不是很适合使用在移动设备与PC之间的结合上，但是能够满足自己的需求就是好的东西。

跑题了，下面还是先说一下SublimeText和PlainTask这东西吧。

## Package Control
### 如何为Sublime Text添加Package Control？
Sublime Text的软件架构支持添加插件，但是我们仍然需要一个方便的管理工具来管理我们的Package，此时我们就需要使用[Package Control](http://wbond.net/sublime_packages/package_control)。

#### 自动安装
按组合键Ctrl+`打开Console，然后添加下面的命令：

    import urllib2,os; pf='Package Control.sublime-package'; ipp=sublime.installed_packages_path(); os.makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read()); print 'Please restart Sublime Text to finish installation'

最新版本的Package Control已经完善了网络代理的功能，因此如果使用时的网络环境处于代理环境下，我们可以通过修改Package Control的配置文件来添加代理服务器地址。

#### 手动安装
1. 点击*Preference > Browse Packages..*
2. 打开*Installed Packages*目录
3. [点击下载](http://sublime.wbond.net/Package%20Control.sublime-package)并将文件复制到'Installed Packages'目录下
4. 重启Sublime Text

#### 如何使用
Package Control安装完成之后，会在软件全局菜单（Ctrl+Shift+p）添加相应的菜单项，我们只需调出菜单，输入pci(for Package Control: Install Package)即可开始安装我们需要的插件。

除此之外还有另外的一些管理插件的命令可以调用，只需简单关注一下相应的菜单选项即可了解。

## PlainTask and PlainTaskOF(Theme)
有了Package Control，我们就可以添加很多强大的插件，例如下面介绍的PlainTask，可以将Sublime Text变身成为一个方便的任务管理软件。

关于PlainTask，可以点击下面的链接看一下Lucifr上面的[介绍文章](http://lucifr.com/2012/09/18/sublime-text-extension-plaintasks/)。看完之后大概会有一个了解，能不能适合自己的情况，这样就见仁见智了。

在Package Control中安装完PlainTask之后，可以在全局菜单中输入*Task*，查看相关的命令。另外一个比较好用的就是，PlainTask里面的快捷键可以帮助我们快捷添加、整理和归档任务列表。不过这个插件的缺点也很明显：没有提醒功能，没有快速采集内容的功能，基本只能靠自己整理。

另外，还有人专门做了一个OmniFocus的配色，很漂亮，可以在这个[Github](https://github.com/poritsky/PlainTasksOF)里面下载tasks-OF.hidden-tmTheme，放置到PlainTask中，然后修改PlainTask的配置文件完成配色主题的修改。

而我做了一个简单的Snippet，方便我们在添加新的任务列表时创建新任务模板，[点击这里](http://d.pr/f/A55t)下载。下载后放置到*Packages/User/*目录下，创建新的Task文件后输入task，轻敲tab即可创建一个列表。

![PlainTaskOF][PTOF]
[PTOF]:http://cdn.lucifr.com/uploads/PlainTasksOF.jpg

## Write Markdown format text in Sublime Text
在Sublime Text中书写Markdown其实也不是十分方便，不过鉴于Windows下面没有像OSX上的Mou那样方便漂亮的Markdown编辑App（有一个叫MarkdownPad的东西，不过没有Markdown语法高亮，感觉不大方便，虽然有很多快捷键辅助。），所以还是尽量用一下Sublime Text吧。

在ST中编辑Markdown有几个比较好的插件，在Package Control中可以下载：
* SmartMarkdown - 提供创建简单表格、智能列表的功能
* MarkdownBuild - 将Markdown转换成HTML文件
* Markdown to Clipboard - 将Markdown转换成HTML代码，用于发布文章
* MarkdownEditing - 与SmartMarkdown类似的插件，但暂时不兼容Windows，有兴趣可以在[Github](https://github.com/ttscoff/MarkdownEditing)上Fork一下

不过MarkdownEditing这个插件提供了一个比较漂亮的Markdown语法高亮主题，可以点击[这里](http://d.pr/f/MQEy)下载，解压放置到*Package/User*目录下即可。

## Git version control and SkyDrive sync

由于我的GTD系统都使用纯文本配置，因此可以考虑给它添加一个版本控制和同步功能。同步软件有很多，这个我就不多说了，你喜欢用Dropbox也好，用Google Drive也好，用iCloud也好，用SkyDrive也好，只要你可以达到同步的效果就可以了。当然，有的同步软件还提供了版本控制的功能，以前用过一个叫Oxygen的软件就是这样，不过同步速度太慢了，比SkyDrive还慢，因此不考虑它了。如果考虑到一个比较适合国内的情况的话，可以用一下金山快盘、551之类的，也还算可以。

在同步软件里面按你需要的分类建立相应的文件夹就可以了，你也可以把一个文件夹看作一个项目，在文件夹里面按照项目的需要建立自己的任务列表文件，然后在Sublime Text中添加相应的文件夹，就可以享受ST那快速切换文件的功能，很好很强大。

另外，如果需要添加版本控制系统，可以直接使用现在很流行的Git。Windows下面安装一个也不难，只需要去下载一个Git Extensions就可以完成整个安装流程了（也可以装一个TortoiseGit，不过感觉速度没Git Extensions那么快）。如果要在ST中集成Git功能的话，可以在Package Control中添加*Git*和*SideBarGit*两个插件，前者是将系统集成的Git命令添加到全局命令菜单中，后者则是强化侧边栏的右键菜单，看你怎么用了。

在我们的文件夹里面建立一个Repo就可以了，然后就可以开始用我们的版本控制系统了。这个Repo一般不大，因为我们存放的都只是一些纯文本文件，用SkyDrive来同步也很快，每次更新也就几KB的事情，方便快捷。

## 我说完了

说到这里，有人会觉得，这不是瞎扯吗？其实我也觉得这种任务管理的方法很扯淡，不过还是那句：适合自己的东西就是最好的。你喜欢吗？反正我觉得这方法挺装B的，虽然用着可能会让别人觉得你很2。



