date: 2013-07-02 14:57
title: Package Control 插件发布流程
permalink: a-brief-about-submitting-a-package-to-package-control
tags: st2
---

Package Control 是 Sublime Text 下的一个插件管理工具，可以很方便地管理需要安装的 Sublime Text 插件。现在已经有不少开发者在上面发布了[各式各样的插件](http://blog.edi-c.com/post/my-st2-tips)，对 Sublime Text 本身的扩展还是很有用的。Sublime Text 本身采用了 Python 作为插件编写的语言，因此在插件开发过程中也十分的轻松，可以实时调试插件的效果。

前两天尝试在上面发布了自己的插件 [ScriptOgrSender](https://github.com/blastmann/ScriptOgrSender)，提交过程也十分简单，下面简单整理一下：

1.  **在 [GitHub](https://github.com/) 或 [BitBucket](https://bitbucket.org/) 中托管你的插件代码。**单个 Repo 只能包含一个插件，同时需要将插件脚本放置于 Repo 的根目录下。
2.  **请勿在你的 Repo 中包含 `package-metadata.json` 文件。**这个文件会在每台客户端中自行创建，用于跟踪安装包的版本。如需对你的插件包描述进行修改，可以在你的 GitHub 和 BitBucket 仓库中修改相应的描述字段。
3.  **Fork the Package Control Channel:  **  
GitHub: [https://github.com/wbond/package_control_channel](https://github.com/wbond/package_control_channel)  
BitBucket: [https://bitbucket.org/wbond/package_control_channel](https://bitbucket.org/wbond/package_control_channel)
4.  **在 `repositories.json` 文件中添加你的 repo URL。**如果你的插件不是在三个平台（OS X, Windows 和 Linux）下面通用的话，请参阅「[在 GitHub 上自定义 packages.json](http://wbond.net/sublime_packages/package_control/package_developers#Custom_packages_json_on_GitHub)」一节。

    添加的 URL 格式请参考下面几种形式：

    - https://github.com/user/repo
    - https://github.com/user/repo/tree/branch
    - https://bitbucket.org/user/repo

    添加你的 URL 时请注意按字母顺序排列添加，以防产生冲突。同时请注意不要在 URL 尾部添加 `.git`。

5.  **在 `package_name_map` 中添加自己的插件包名字的映射（可选）。**注意，如果你没有自定义 `packages.json` 文件而且不想用你的 GitHub Repo 的 URL permalink 作为你的插件名字的话，请务必将你想要的插件名字添加到此字段中。如插件托管在 BitBucket 的话，将使用 Repo 的名字，不需要再另外添加映射。

    **如果你的插件名中包含 *Sublime* 这个字眼的话，请考虑映射另外一个名字（去除 *Sublime*）以减少信息噪音。**这里的映射会在 Community Package 列表、ST 中的安装列表和安装后的文件夹名字中生效。

6.  **修改时请确保你的修改不会影响其它代码。**
7.  **发送一个 Pull 请求。**

整个提交过程十分简单，我也是第一次在 GitHub 上对其它代码仓库进行代码提交（其实就加了那么一行），提交时还没有注意到添加的 URL 必须按字母顺序排列，结果被打回来再修改了一次。

之前做的插件在跨平台方面也没有什么问题，所以整个代码提交过程也十分轻松，不用特别去制件一个专属的 JSON 文件。只要加入 Package Control 之后，就可以继续在自己的 Repo 中进行代码更新。Package Control 会自动拉取新的代码更新插件包，过程大概需要一两个小时吧。

至于怎么去针对 ST2 和 ST3 进行插件发布呢？这个问题还没有研究清楚，过两天看看怎么处理吧。